import os
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from gridfs import GridFS
from pymongo import DESCENDING
from pymongo.database import Database

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.mongo import next_sequence, strip_mongo_id, with_timestamps
from app.db.session import get_db
from app.schemas.menu import UploadRecordRead, UploadResponse
from app.services.menu_parser import normalize_menu_text
from app.services.nutrition import enrich_menu_items
from app.services.ocr import extract_text_from_upload

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", response_model=list[UploadRecordRead])
def list_uploads(
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[dict]:
    uploads = list(
        db.upload_records.find({"user_id": current_user["id"]}, {"_id": 0}).sort(
            "created_at", DESCENDING
        )
    )
    return [_serialize_upload_record(record, db) for record in uploads]


@router.get("/{upload_id}", response_model=UploadRecordRead)
def get_upload(
    upload_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    record = strip_mongo_id(
        db.upload_records.find_one({"id": upload_id, "user_id": current_user["id"]})
    )
    if not record:
        raise HTTPException(status_code=404, detail="Upload not found")
    return _serialize_upload_record(record, db)


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
                "notes": "File stored successfully. Waiting for local OCR/text extraction.",
            }
        )
    )

    try:
        extracted_text = extract_text_from_upload(file.filename or "menu", contents)
        if not extracted_text.strip():
            raise RuntimeError(
                "No readable text was found in the uploaded file. Try a text PDF or a clearer image."
            )
        structured = normalize_menu_text(extracted_text)
        analyzed_items = enrich_menu_items(structured.get("items", []))
        structured["items"] = analyzed_items
    except Exception as exc:
        logger.exception("Local upload analysis failed for upload: %s", file.filename)
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
            "extracted_text": extracted_text,
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
                        "File stored successfully, then parsed with local OCR/text extraction "
                        "and rule-based nutrition estimation."
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


def _serialize_upload_record(record: dict, db: Database) -> dict:
    menu = None
    if record.get("menu_id"):
        menu = strip_mongo_id(db.menus.find_one({"id": record["menu_id"]}))

    extracted_text = None
    if menu:
        extracted_text = menu.get("extracted_text")

    return {
        "id": record["id"],
        "user_id": record["user_id"],
        "menu_id": record.get("menu_id"),
        "file_name": record.get("file_name"),
        "file_type": record.get("file_type"),
        "source_url": record.get("source_url"),
        "processing_status": record.get("processing_status", "unknown"),
        "notes": record.get("notes"),
        "file_path": record.get("file_path"),
        "extracted_preview": extracted_text[:500] if extracted_text else None,
        "created_at": record["created_at"].isoformat(),
        "updated_at": record["updated_at"].isoformat(),
    }
