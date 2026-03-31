import logging

from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.mongo import next_sequence, with_timestamps
from app.db.session import get_db
from app.schemas.recommendation import RecommendationResponse, RecommendationResult
from app.services.openai_analysis import generate_ai_recommendations

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/{menu_id}", response_model=RecommendationResponse)
def recommend_for_menu(
    menu_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> RecommendationResponse:
    if not current_user.get("profile"):
        raise HTTPException(
            status_code=400, detail="Profile setup is required before recommendations."
        )

    menu = db.menus.find_one({"id": menu_id}, {"_id": 0})
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    menu_items = list(db.menu_items.find({"menu_id": menu_id}, {"_id": 0}))
    if not menu_items:
        raise HTTPException(status_code=400, detail="No menu items were extracted for this menu.")

    try:
        result = generate_ai_recommendations(current_user["profile"], menu_items)
    except RuntimeError as exc:
        logger.exception("Recommendation generation unavailable")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("AI recommendation generation failed for menu_id=%s", menu_id)
        raise HTTPException(
            status_code=502,
            detail=(
                str(exc)
                if settings.env == "development"
                else "AI recommendation generation failed for this menu."
            ),
        ) from exc

    for bucket_name, rec_type in (
        ("top_recommendations", "top_pick"),
        ("alternatives", "alternative"),
        ("dishes_to_avoid", "avoid"),
    ):
        for entry in result[bucket_name]:
            db.recommendations.insert_one(
                with_timestamps(
                    {
                        "id": next_sequence(db, "recommendations"),
                        "user_id": current_user["id"],
                        "menu_item_id": entry["menu_item_id"],
                        "recommendation_type": rec_type,
                        "match_score": entry["match_score"],
                        "summary_reason": entry["summary_reason"],
                        "why_recommended": entry["why_recommended"],
                        "why_not_recommended": entry["why_not_recommended"],
                        "warnings": entry["warnings"],
                        "saved": False,
                    }
                )
            )

    return RecommendationResponse(
        disclaimer=result["disclaimer"],
        top_recommendations=[
            RecommendationResult(**item) for item in result["top_recommendations"]
        ],
        alternatives=[RecommendationResult(**item) for item in result["alternatives"]],
        dishes_to_avoid=[
            RecommendationResult(**item) for item in result["dishes_to_avoid"]
        ],
    )
