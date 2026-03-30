from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.api.deps import get_current_user
from app.db.mongo import next_sequence, strip_mongo_id, with_timestamps
from app.db.session import get_db
from app.schemas.profile import UserProfileCreate, UserProfileRead

router = APIRouter()


@router.get("", response_model=UserProfileRead | None)
def get_profile(current_user: dict = Depends(get_current_user)) -> dict | None:
    if current_user.get("profile"):
        current_user["profile"].setdefault("preferred_dining_styles", [])
    return current_user.get("profile")


@router.put("", response_model=UserProfileRead)
def upsert_profile(
    payload: UserProfileCreate,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    profile = current_user.get("profile")
    data = payload.model_dump(exclude={"user_id"})

    if profile:
        db.user_profiles.update_one(
            {"user_id": current_user["id"]},
            {"$set": with_timestamps(data, update=True)},
        )
    else:
        profile = with_timestamps(
            {
                "id": next_sequence(db, "user_profiles"),
                "user_id": current_user["id"],
                **data,
            }
        )
        db.user_profiles.insert_one(profile)

    profile = strip_mongo_id(db.user_profiles.find_one({"user_id": current_user["id"]}))
    if profile:
        profile.setdefault("preferred_dining_styles", [])
    return profile
