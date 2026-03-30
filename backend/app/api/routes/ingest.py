from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.api.deps import get_current_user
from app.db.mongo import next_sequence, strip_mongo_id, with_timestamps
from app.db.session import get_db
from app.schemas.menu import MenuRead, UrlIngestRequest
from app.services.nutrition import enrich_menu_items
from app.services.web_ingestion import crawl_restaurant_menu

router = APIRouter()


@router.post("/url", response_model=MenuRead)
def ingest_url(
    payload: UrlIngestRequest,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> MenuRead:
    result = crawl_restaurant_menu(str(payload.url))
    enriched_items = enrich_menu_items(result["items"])
    result["items"] = enriched_items

    restaurant_id = next_sequence(db, "restaurants")
    db.restaurants.insert_one(
        with_timestamps(
            {
                "id": restaurant_id,
                "name": result["restaurant_name"],
                "website_url": str(payload.url),
                "cuisine_tags": result.get("cuisine_tags", []),
                "source_type": "url",
            }
        )
    )

    menu_id = next_sequence(db, "menus")
    db.menus.insert_one(
        with_timestamps(
            {
                "id": menu_id,
                "restaurant_id": restaurant_id,
                "source_type": "url",
                "source_url": str(payload.url),
                "source_filename": None,
                "extracted_text": result.get("raw_text"),
                "structured_json": result,
            }
        )
    )

    for item in enriched_items:
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

    db.upload_records.insert_one(
        with_timestamps(
            {
                "id": next_sequence(db, "upload_records"),
                "user_id": current_user["id"],
                "menu_id": menu_id,
                "file_name": None,
                "file_type": "url",
                "source_url": str(payload.url),
                "processing_status": "completed",
                "notes": "Parsed with sample restaurant website parser logic.",
            }
        )
    )

    menu = strip_mongo_id(db.menus.find_one({"id": menu_id}))
    menu["items"] = [
        strip_mongo_id(item) for item in db.menu_items.find({"menu_id": menu_id}, {"_id": 0})
    ]
    return menu
