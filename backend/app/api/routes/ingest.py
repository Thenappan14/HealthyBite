from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Menu, MenuItem, Restaurant, UploadRecord, User
from app.schemas.menu import MenuRead, UrlIngestRequest
from app.services.nutrition import enrich_menu_items
from app.services.web_ingestion import crawl_restaurant_menu

router = APIRouter()


@router.post("/url", response_model=MenuRead)
def ingest_url(
    payload: UrlIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MenuRead:
    result = crawl_restaurant_menu(str(payload.url))
    enriched_items = enrich_menu_items(result["items"])
    result["items"] = enriched_items

    restaurant = Restaurant(
        name=result["restaurant_name"],
        website_url=str(payload.url),
        cuisine_tags=result.get("cuisine_tags", []),
        source_type="url",
    )
    db.add(restaurant)
    db.flush()

    menu = Menu(
        restaurant_id=restaurant.id,
        source_type="url",
        source_url=str(payload.url),
        extracted_text=result.get("raw_text"),
        structured_json=result,
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
        file_type="url",
        source_url=str(payload.url),
        processing_status="completed",
        notes="Parsed with sample restaurant website parser logic.",
    )
    db.add(upload)
    db.commit()
    db.refresh(menu)
    return menu

