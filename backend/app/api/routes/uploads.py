import os
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pymongo.database import Database

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.mongo import next_sequence, with_timestamps
from app.db.session import get_db
from app.schemas.menu import UploadResponse
from app.services.openai_analysis import analyze_uploaded_menu

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=UploadResponse)
async def upload_menu(
    file: UploadFile = File(...),
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".pdf", ".webp"}:
        raise HTTPException(status_code=400, detail="Only images and PDFs are supported.")

    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = Path(settings.upload_dir) / (file.filename or "menu-upload")
    contents = await file.read()
    file_path.write_bytes(contents)

    try:
        structured = analyze_uploaded_menu(file.filename or "menu", contents)
    except RuntimeError as exc:
        logger.exception("Upload menu analysis unavailable")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("AI menu extraction failed for upload: %s", file.filename)
        raise HTTPException(
            status_code=502,
            detail=(
                str(exc)
                if settings.env == "development"
                else "AI menu extraction failed for this upload. Try a clearer file or retry."
            ),
        ) from exc

    analyzed_items = structured.get("items", [])
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

    menu_id = next_sequence(db, "menus")
    menu = with_timestamps(
        {
            "id": menu_id,
            "restaurant_id": None,
            "source_type": "upload",
            "source_filename": file.filename,
            "source_url": None,
            "extracted_text": extracted_preview,
            "structured_json": structured,
        }
    )
    db.menus.insert_one(menu)

    for item in analyzed_items:
        db.menu_items.insert_one(
            with_timestamps(
                {
                    "id": next_sequence(db, "menu_items"),
                    "menu_id": menu_id,
                    "category": item.get("category"),
                    "name": item["name"],
                    "description": item.get("description"),
                    "price": item.get("price"),
                    "inferred_ingredients": item.get("inferred_ingredients", []),
                    "nutrition_estimate": item.get("nutrition_estimate", {}),
                    "allergens": item.get("allergens", []),
                    "diet_compatibility": item.get("diet_compatibility", []),
                    "confidence_score": item.get("confidence_score", 0.5),
                }
            )
        )

    upload_id = next_sequence(db, "upload_records")
    db.upload_records.insert_one(
        with_timestamps(
            {
                "id": upload_id,
                "user_id": current_user["id"],
                "menu_id": menu_id,
                "file_name": file.filename,
                "file_type": suffix.replace(".", ""),
                "source_url": None,
                "processing_status": "completed",
                "notes": (
                    "Analyzed with OpenAI vision/document understanding and structured "
                    "estimated nutrition extraction."
                ),
            }
        )
    )
    return UploadResponse(
        upload_id=upload_id,
        menu_id=menu_id,
        extracted_preview=extracted_preview[:300],
    )
