from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title="PlateWise API",
    version="0.1.0",
    description=(
        "PlateWise provides estimated nutrition analysis and personalized menu "
        "recommendations based on user profile information."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "name": "PlateWise API",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health",
        "api_base": "/api",
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> None:
    return None


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
