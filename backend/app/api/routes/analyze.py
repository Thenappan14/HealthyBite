import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from gridfs import GridFS
from pymongo.database import Database

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.mongo import next_sequence, with_timestamps
from app.db.session import get_db
from app.schemas.menu import UploadRecordRead
from app.schemas.recommendation import RecommendationResponse, RecommendationResult
from app.services.menu_parser import normalize_menu_document
from app.services.nutrition import enrich_menu_items
from app.services.ocr import extract_document_payload
from app.services.recommender import build_menu_item_models, build_profile_model, generate_recommendations

router = APIRouter()
logger = logging.getLogger(__name__)


class AnalyzeResponse(RecommendationResponse):
    """Combined response: upload info + recommendations"""
    upload_id: int
    menu_id: int
    upload_filename: str
    extracted_preview: str


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_menu_with_restrictions(
    file: UploadFile = File(...),
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> AnalyzeResponse:
    """
    Combined endpoint: upload menu → extract → enrich → rank by dietary restrictions.
    
    Returns upload info + ranked recommendations in one call.
    """
    if not current_user.get("profile"):
        raise HTTPException(
            status_code=400, detail="Profile setup is required before analysis."
        )

    # Validate file type
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".pdf", ".webp"}:
        raise HTTPException(status_code=400, detail="Only images and PDFs are supported.")

    # Step 1: Store upload record
    upload_id = next_sequence(db, "upload_records")
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(settings.upload_dir) / f"{upload_id}-{file.filename or 'menu-upload'}"
    contents = await file.read()
    file_path.write_bytes(contents)
    
    gridfs_id = GridFS(db).put(
        contents,
        filename=file.filename or f"upload-{upload_id}",
        content_type=file.content_type or "application/octet-stream",
    )

    db.upload_records.insert_one(
        with_timestamps(
            {
                "id": upload_id,
                "user_id": current_user["id"],
                "menu_id": None,
                "file_name": file.filename,
                "file_type": suffix.replace(".", ""),
                "source_url": None,
                "processing_status": "processing",
                "file_path": str(file_path),
                "file_storage": {
                    "gridfs_id": str(gridfs_id),
                    "content_type": file.content_type or "application/octet-stream",
                },
                "notes": "Analyzing menu with dietary restrictions.",
            }
        )
    )

    try:
        # Step 2: Extract text from document
        document_payload = extract_document_payload(file.filename or "menu", contents)
        extracted_text = document_payload["text"]
        if not extracted_text.strip():
            raise RuntimeError(
                "No readable text was found in the uploaded file. Try a text PDF or a clearer image."
            )

        # Step 3: Normalize and enrich menu items
        structured = normalize_menu_document(document_payload)
        analyzed_items = enrich_menu_items(structured.get("items", []))
        structured["items"] = analyzed_items

        # Step 4: Create menu in database
        menu_id = next_sequence(db, "menus")
        menu = with_timestamps(
            {
                "id": menu_id,
                "restaurant_id": None,
                "source_type": "upload",
                "source_filename": file.filename,
                "source_url": None,
                "extracted_text": extracted_text,
                "structured_json": structured,
            }
        )
        db.menus.insert_one(menu)

        # Step 5: Store menu items in database
        for item in analyzed_items:
            menu_item_id = next_sequence(db, "menu_items")
            db.menu_items.insert_one(
                with_timestamps(
                    {
                        "id": menu_item_id,
                        "menu_id": menu_id,
                        "name": item.get("name", "Unknown Dish"),
                        "category": item.get("category"),
                        "description": item.get("description"),
                        "price": item.get("price"),
                        "source_page": item.get("source_page"),
                        "source_text": item.get("source_text"),
                        "nutrition_estimate": item.get("nutrition_estimate", {}),
                        "allergens": item.get("allergens", []),
                        "inferred_ingredients": item.get("inferred_ingredients", []),
                        "diet_compatibility": item.get("diet_compatibility", []),
                        "confidence_score": item.get("confidence_score", 0.0),
                    }
                )
            )

        # Update upload record with menu_id
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "menu_id": menu_id,
                        "processing_status": "completed",
                        "notes": "Menu extracted and enriched successfully.",
                    },
                    update=True,
                )
            },
        )

        # Step 6: Generate recommendations based on user profile
        menu_items = list(db.menu_items.find({"menu_id": menu_id}, {"_id": 0}))
        result = generate_recommendations(
            build_profile_model(current_user["profile"]),
            build_menu_item_models(menu_items),
        )

        # Step 7: Store recommendations in database
        for bucket_name, rec_type in (
            ("top_recommendations", "top_pick"),
            ("alternatives", "alternative"),
            ("dishes_to_avoid", "avoid"),
        ):
            for entry in result[bucket_name]:
                db.recommendations.insert_one(
                    with_timestamps(
                        {
                            "id": next_sequence(db, "recommendations"),
                            "user_id": current_user["id"],
                            "menu_item_id": entry["menu_item_id"],
                            "recommendation_type": rec_type,
                            "match_score": entry["match_score"],
                            "summary_reason": entry["summary_reason"],
                            "why_recommended": entry["why_recommended"],
                            "why_not_recommended": entry["why_not_recommended"],
                            "warnings": entry["warnings"],
                            "saved": False,
                        }
                    )
                )

        # Step 8: Prepare preview text
        extracted_preview = structured.get("source_summary") or (
            "\n".join(
                filter(
                    None,
                    [
                        f'{item.get("name", "")}: {item.get("description", "")}'.strip(": ")
                        for item in analyzed_items[:5]
                    ],
                )
            )
        )

        # Return combined response
        return AnalyzeResponse(
            upload_id=upload_id,
            menu_id=menu_id,
            upload_filename=file.filename or "menu",
            extracted_preview=extracted_preview,
            disclaimer=result["disclaimer"],
            top_recommendations=[
                RecommendationResult(**item) for item in result["top_recommendations"]
            ],
            alternatives=[
                RecommendationResult(**item) for item in result["alternatives"]
            ],
            dishes_to_avoid=[
                RecommendationResult(**item) for item in result["dishes_to_avoid"]
            ],
        )

    except Exception as exc:
        logger.exception("Combined analysis failed for upload: %s", file.filename)
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "processing_status": "failed",
                        "notes": str(exc),
                    },
                    update=True,
                )
            },
        )
        raise HTTPException(
            status_code=422,
            detail={
                "message": str(exc),
                "upload_id": upload_id,
                "stored": True,
            },
        ) from exc
