from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User, UserProfile
from app.schemas.profile import UserProfileCreate, UserProfileRead

router = APIRouter()


@router.get("", response_model=UserProfileRead | None)
def get_profile(current_user: User = Depends(get_current_user)) -> UserProfile | None:
    return current_user.profile


@router.put("", response_model=UserProfileRead)
def upsert_profile(
    payload: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProfile:
    profile = current_user.profile
    data = payload.model_dump(exclude={"user_id"})

    if profile:
        for key, value in data.items():
            setattr(profile, key, value)
    else:
        profile = UserProfile(user_id=current_user.id, **data)
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile

