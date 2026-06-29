from pathlib import Path
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"


def _read_file_openai_values() -> dict[str, str]:
    field_names = {
        "OPENAI_API_KEY": "openai_api_key",
        "OPENAI_ORGANIZATION": "openai_organization",
        "OPENAI_PROJECT": "openai_project",
        "OPENAI_MENU_MODEL": "openai_menu_model",
        "OPENAI_RECOMMENDATION_MODEL": "openai_recommendation_model",
    }
    if not ENV_FILE.exists():
        return {}

    values: dict[str, str] = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        field_name = field_names.get(key.strip())
        if field_name:
            values[field_name] = value.strip().strip('"').strip("'")
    return values


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
        if isinstance(value, str) and value.startswith("OPENAI_API_KEY="):
            return value.removeprefix("OPENAI_API_KEY=").strip()
        return value

    def __init__(self, **data):
        file_openai_values = _read_file_openai_values()
        for field_name, value in file_openai_values.items():
            if field_name not in data and value and value.strip():
                data[field_name] = value
        super().__init__(**data)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
