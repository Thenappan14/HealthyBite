from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pymongo.database import Database

from app.api.deps import get_current_user
from app.db.mongo import next_sequence, strip_mongo_id, with_timestamps
from app.db.session import get_db
from app.schemas.menu import MenuRead, UrlIngestRequest
from app.services.openai_analysis import analyze_restaurant_url
from app.services.web_ingestion import crawl_restaurant_menu

router = APIRouter()


@router.post("/url", response_model=MenuRead)
def ingest_url(
    payload: UrlIngestRequest,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> MenuRead:
    website_context = crawl_restaurant_menu(str(payload.url))
    combined_source_text = "\n\n".join(
        filter(
            None,
            [
                website_context.get("raw_text"),
                website_context.get("html_excerpt"),
                "\n".join(website_context.get("parser_notes", [])),
            ],
        )
    )
    try:
        result = analyze_restaurant_url(str(payload.url), combined_source_text)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="AI website menu extraction failed for this restaurant URL.",
        ) from exc

    analyzed_items = result.get("items", [])

    restaurant_id = next_sequence(db, "restaurants")
    db.restaurants.insert_one(
        with_timestamps(
            {
                "id": restaurant_id,
                "name": result.get("restaurant_name") or "Unknown restaurant",
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
                "extracted_text": result.get("source_summary"),
                "structured_json": result,
            }
        )
    )

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
                "notes": (
                    "Fetched website text and analyzed with OpenAI for structured menu extraction "
                    "and estimated nutrition."
                ),
            }
        )
    )

    menu = strip_mongo_id(db.menus.find_one({"id": menu_id}))
    menu["items"] = [
        strip_mongo_id(item) for item in db.menu_items.find({"menu_id": menu_id}, {"_id": 0})
    ]
    return menu
