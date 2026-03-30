from fastapi import APIRouter, Depends
from pymongo import DESCENDING
from pymongo.database import Database

from app.api.deps import get_current_user
from app.db.session import get_db

router = APIRouter()


@router.get("")
def get_history(
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[dict]:
    recommendations = list(
        db.recommendations.find({"user_id": current_user["id"]}, {"_id": 0}).sort(
            "created_at", DESCENDING
        )
    )

    history = []
    for rec in recommendations:
        menu_item = db.menu_items.find_one({"id": rec["menu_item_id"]}, {"_id": 0})
        history.append(
            {
                "id": rec["id"],
                "type": rec["recommendation_type"],
                "score": rec["match_score"],
                "dish_name": menu_item["name"] if menu_item else "Unknown item",
                "summary_reason": rec["summary_reason"],
                "warnings": rec.get("warnings", []),
                "saved": rec.get("saved", False),
                "created_at": rec["created_at"].isoformat(),
            }
        )
    return history
