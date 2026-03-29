from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Menu, Recommendation, User
from app.schemas.recommendation import RecommendationResponse, RecommendationResult
from app.services.recommender import generate_recommendations

router = APIRouter()


@router.post("/{menu_id}", response_model=RecommendationResponse)
def recommend_for_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RecommendationResponse:
    if not current_user.profile:
        raise HTTPException(
            status_code=400, detail="Profile setup is required before recommendations."
        )

    menu = db.query(Menu).options(selectinload(Menu.items)).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    result = generate_recommendations(current_user.profile, menu.items)

    for bucket_name, rec_type in (
        ("top_recommendations", "top_pick"),
        ("alternatives", "alternative"),
        ("dishes_to_avoid", "avoid"),
    ):
        for entry in result[bucket_name]:
            db.add(
                Recommendation(
                    user_id=current_user.id,
                    menu_item_id=entry["menu_item_id"],
                    recommendation_type=rec_type,
                    match_score=entry["match_score"],
                    summary_reason=entry["summary_reason"],
                    why_recommended=entry["why_recommended"],
                    why_not_recommended=entry["why_not_recommended"],
                    warnings=entry["warnings"],
                )
            )

    db.commit()

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

