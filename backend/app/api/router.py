from fastapi import APIRouter

from app.api.routes import auth, history, ingest, menus, profile, recommendations, uploads

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)
api_router.include_router(history.router, prefix="/history", tags=["history"])
