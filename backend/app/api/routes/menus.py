from fastapi import APIRouter, Depends, HTTPException
from pymongo import DESCENDING
from pymongo.database import Database

from app.api.deps import get_current_user
from app.db.mongo import strip_mongo_id
from app.db.session import get_db
from app.schemas.menu import MenuRead

router = APIRouter()


@router.get("", response_model=list[MenuRead])
def list_menus(
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[dict]:
    uploads = list(
        db.upload_records.find({"user_id": current_user["id"]}, {"_id": 0}).sort(
            "created_at", DESCENDING
        )
    )
    menu_ids: list[int] = []
    for upload in uploads:
        menu_id = upload.get("menu_id")
        if menu_id and menu_id not in menu_ids:
            menu_ids.append(menu_id)

    results: list[dict] = []
    for menu_id in menu_ids:
        menu = strip_mongo_id(db.menus.find_one({"id": menu_id}))
        if not menu:
            continue
        menu["items"] = [
            strip_mongo_id(item) for item in db.menu_items.find({"menu_id": menu_id}, {"_id": 0})
        ]
        results.append(menu)
    return results


@router.get("/{menu_id}", response_model=MenuRead)
def get_menu(
    menu_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    upload = db.upload_records.find_one({"user_id": current_user["id"], "menu_id": menu_id})
    if not upload:
        raise HTTPException(status_code=404, detail="Menu not found for this user")

    menu = strip_mongo_id(db.menus.find_one({"id": menu_id}))
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    menu["items"] = [
        strip_mongo_id(item) for item in db.menu_items.find({"menu_id": menu_id}, {"_id": 0})
    ]
    return menu
