from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Recommendation, User

router = APIRouter()


@router.get("")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[dict]:
    recommendations = (
        db.query(Recommendation)
        .options(joinedload(Recommendation.menu_item))
        .filter(Recommendation.user_id == current_user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    return [
        {
            "id": rec.id,
            "type": rec.recommendation_type,
            "score": rec.match_score,
            "dish_name": rec.menu_item.name,
            "summary_reason": rec.summary_reason,
            "warnings": rec.warnings,
            "saved": rec.saved,
            "created_at": rec.created_at.isoformat(),
        }
        for rec in recommendations
    ]
