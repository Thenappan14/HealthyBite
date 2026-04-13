import os
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PlateWise"
    env: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "platewise"
    openai_api_key: str | None = None
    openai_organization: str | None = None
    openai_project: str | None = None
    openai_menu_model: str = "gpt-4.1"
    openai_recommendation_model: str = "gpt-4.1"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    frontend_url: str = "http://localhost:3000"
    upload_dir: str = "storage/uploads"
    max_upload_size_mb: int = 10

    @field_validator("openai_api_key", "openai_organization", "openai_project", mode="before")
    @classmethod
    def _normalize_optional_openai_values(cls, value: str | None) -> str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    def __init__(self, **data):
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key and env_key.strip():
            data["openai_api_key"] = env_key
        super().__init__(**data)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
