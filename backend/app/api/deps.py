from fastapi import Depends, Header, HTTPException, status
from pymongo.database import Database

from app.db.session import get_db


def get_current_user(
    db: Database = Depends(get_db),
    x_user_id: int | None = Header(default=None),
) -> dict:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provide X-User-Id header for the current signed-in user.",
        )

    user = db.users.find_one({"id": x_user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user["profile"] = db.user_profiles.find_one({"user_id": x_user_id}, {"_id": 0})
    if user["profile"]:
        user["profile"].setdefault("preferred_dining_styles", [])
    return user
