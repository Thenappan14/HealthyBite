from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PlateWise"
    env: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "platewise"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    frontend_url: str = "http://localhost:3000"
    upload_dir: str = "storage/uploads"
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
