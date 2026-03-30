from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.mongo import next_sequence, with_timestamps
from app.db.session import get_db
from app.schemas.auth import LoginRequest, SignUpRequest, TokenResponse

router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
def signup(payload: SignUpRequest, db: Database = Depends(get_db)) -> TokenResponse:
    existing = db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user_id = next_sequence(db, "users")
    db.users.insert_one(
        with_timestamps(
            {
                "id": user_id,
                "email": payload.email,
                "hashed_password": get_password_hash(payload.password),
            }
        )
    )
    return TokenResponse(access_token=create_access_token(str(user_id)), user_id=user_id)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Database = Depends(get_db)) -> TokenResponse:
    user = db.users.find_one({"email": payload.email}, {"_id": 0})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return TokenResponse(access_token=create_access_token(str(user["id"])), user_id=user["id"])
