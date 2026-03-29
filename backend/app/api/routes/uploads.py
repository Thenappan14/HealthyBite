import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models import Menu, MenuItem, UploadRecord, User
from app.schemas.menu import UploadResponse
from app.services.menu_parser import normalize_menu_text
from app.services.nutrition import enrich_menu_items
from app.services.ocr import extract_text_from_upload

router = APIRouter()


@router.post("", response_model=UploadResponse)
async def upload_menu(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".pdf", ".webp"}:
        raise HTTPException(status_code=400, detail="Only images and PDFs are supported.")

    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = Path(settings.upload_dir) / (file.filename or "menu-upload")
    contents = await file.read()
    file_path.write_bytes(contents)

    extracted_text = extract_text_from_upload(file.filename or "menu", contents)
    structured = normalize_menu_text(extracted_text)
    enriched_items = enrich_menu_items(structured["items"])
    structured["items"] = enriched_items

    menu = Menu(
        source_type="upload",
        source_filename=file.filename,
        extracted_text=extracted_text,
        structured_json=structured,
    )
    db.add(menu)
    db.flush()

    for item in enriched_items:
        db.add(
            MenuItem(
                menu_id=menu.id,
                category=item.get("category"),
                name=item["name"],
                description=item.get("description"),
                price=item.get("price"),
                inferred_ingredients=item.get("inferred_ingredients", []),
                nutrition_estimate=item.get("nutrition_estimate", {}),
                allergens=item.get("allergens", []),
                diet_compatibility=item.get("diet_compatibility", []),
                confidence_score=item.get("confidence_score", 0.5),
            )
        )

    upload = UploadRecord(
        user_id=current_user.id,
        menu_id=menu.id,
        file_name=file.filename,
        file_type=suffix.replace(".", ""),
        processing_status="completed",
        notes="Parsed with rule-based OCR placeholder pipeline.",
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return UploadResponse(
        upload_id=upload.id,
        menu_id=menu.id,
        extracted_preview=extracted_text[:300],
    )

