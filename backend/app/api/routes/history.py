from fastapi import APIRouter, Depends, HTTPException
from pymongo import DESCENDING
from pymongo.database import Database

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.recommendation import RecommendationHistoryItem, RecommendationSaveRequest

router = APIRouter()


@router.get("", response_model=list[RecommendationHistoryItem])
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


@router.put("/{recommendation_id}/save", response_model=RecommendationHistoryItem)
def save_recommendation(
    recommendation_id: int,
    payload: RecommendationSaveRequest,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    db.recommendations.update_one(
        {"id": recommendation_id, "user_id": current_user["id"]},
        {"$set": {"saved": payload.saved}},
    )
    rec = db.recommendations.find_one(
        {"id": recommendation_id, "user_id": current_user["id"]}, {"_id": 0}
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    menu_item = db.menu_items.find_one({"id": rec["menu_item_id"]}, {"_id": 0})
    return {
        "id": rec["id"],
        "type": rec["recommendation_type"],
        "score": rec["match_score"],
        "dish_name": menu_item["name"] if menu_item else "Unknown item",
        "summary_reason": rec["summary_reason"],
        "warnings": rec.get("warnings", []),
        "saved": rec.get("saved", False),
        "created_at": rec["created_at"].isoformat(),
    }
