import os
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from gridfs import GridFS
from openai import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError
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

    upload_id = next_sequence(db, "upload_records")
    os.makedirs(settings.upload_dir, exist_ok=True)
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
                "notes": "File stored successfully. Waiting for AI extraction.",
            }
        )
    )

    try:
        structured = analyze_uploaded_menu(file.filename or "menu", contents)
    except RuntimeError as exc:
        logger.exception("Upload menu analysis unavailable")
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
            status_code=503,
            detail={"message": str(exc), "upload_id": upload_id, "stored": True},
        ) from exc
    except RateLimitError as exc:
        logger.exception("OpenAI quota exceeded during upload analysis")
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "processing_status": "failed",
                        "notes": "OpenAI quota exceeded during upload analysis.",
                    },
                    update=True,
                )
            },
        )
        raise HTTPException(
            status_code=429,
            detail={
                "message": "OpenAI quota exceeded. Check your OpenAI billing, credits, and project limits.",
                "upload_id": upload_id,
                "stored": True,
            },
        ) from exc
    except AuthenticationError as exc:
        logger.exception("OpenAI authentication failed during upload analysis")
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "processing_status": "failed",
                        "notes": "OpenAI authentication failed during upload analysis.",
                    },
                    update=True,
                )
            },
        )
        raise HTTPException(
            status_code=401,
            detail={
                "message": "OpenAI authentication failed. Check OPENAI_API_KEY in backend/.env.",
                "upload_id": upload_id,
                "stored": True,
            },
        ) from exc
    except APIConnectionError as exc:
        logger.exception("OpenAI connection failed during upload analysis")
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "processing_status": "failed",
                        "notes": "Could not connect to OpenAI from the backend.",
                    },
                    update=True,
                )
            },
        )
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Could not connect to OpenAI from the backend.",
                "upload_id": upload_id,
                "stored": True,
            },
        ) from exc
    except APIStatusError as exc:
        logger.exception("OpenAI API status error during upload analysis")
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "processing_status": "failed",
                        "notes": f"OpenAI API error: {exc.status_code}",
                    },
                    update=True,
                )
            },
        )
        raise HTTPException(
            status_code=502,
            detail={
                "message": (
                    f"OpenAI API error: {exc.status_code}"
                    if settings.env == "development"
                    else "OpenAI API returned an error during upload analysis."
                ),
                "upload_id": upload_id,
                "stored": True,
            },
        ) from exc
    except Exception as exc:
        logger.exception("AI menu extraction failed for upload: %s", file.filename)
        db.upload_records.update_one(
            {"id": upload_id},
            {
                "$set": with_timestamps(
                    {
                        "processing_status": "failed",
                        "notes": (
                            str(exc)
                            if settings.env == "development"
                            else "AI menu extraction failed for this upload."
                        ),
                    },
                    update=True,
                )
            },
        )
        raise HTTPException(
            status_code=502,
            detail={
                "message": (
                    str(exc)
                    if settings.env == "development"
                    else "AI menu extraction failed for this upload. Try a clearer file or retry."
                ),
                "upload_id": upload_id,
                "stored": True,
            },
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

    db.upload_records.update_one(
        {"id": upload_id},
        {
            "$set": with_timestamps(
                {
                    "menu_id": menu_id,
                    "processing_status": "completed",
                    "notes": (
                        "File stored successfully, then analyzed with OpenAI and saved "
                        "as structured estimated nutrition data."
                    ),
                },
                update=True,
            )
        },
    )
    return UploadResponse(
        upload_id=upload_id,
        menu_id=menu_id,
        extracted_preview=extracted_preview[:300],
    )
