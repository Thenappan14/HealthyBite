from __future__ import annotations

from typing import Any

from app.models import MenuItemModel, UserProfileModel
from app.services.openai_analysis import generate_ai_recommendations


def build_profile_model(profile: dict[str, Any]) -> UserProfileModel:
    return UserProfileModel(**profile)


def build_menu_item_models(items: list[dict[str, Any]]) -> list[MenuItemModel]:
    return [MenuItemModel(**item) for item in items]


def generate_recommendations(
    profile: UserProfileModel, items: list[MenuItemModel]
) -> dict[str, Any]:
    return generate_ai_recommendations(
        profile.model_dump(),
        [item.model_dump() for item in items],
    )
