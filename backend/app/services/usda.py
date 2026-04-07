from __future__ import annotations

from functools import lru_cache
from typing import Any

import httpx

from app.core.config import settings


NUTRIENT_KEYS = {
    "1008": "calories",
    "1003": "protein",
    "1005": "carbs",
    "1004": "fat",
    "1079": "fiber",
    "2000": "sugar",
    "1093": "sodium",
}


def lookup_ingredient_nutrition(query: str) -> dict[str, Any] | None:
    if not settings.usda_api_key:
        return None
    return _lookup_ingredient_nutrition_cached(query.strip().lower())


@lru_cache(maxsize=256)
def _lookup_ingredient_nutrition_cached(query: str) -> dict[str, Any] | None:
    if not query:
        return None

    response = httpx.get(
        f"{settings.usda_base_url}/foods/search",
        params={
            "api_key": settings.usda_api_key,
            "query": query,
            "pageSize": 3,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()
    foods = payload.get("foods", [])
    if not foods:
        return None

    best = foods[0]
    nutrients = {
        "calories": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
        "fiber": 0.0,
        "sugar": 0.0,
        "sodium": 0.0,
    }

    for nutrient in best.get("foodNutrients", []):
        nutrient_number = str(nutrient.get("nutrientNumber", ""))
        key = NUTRIENT_KEYS.get(nutrient_number)
        if not key:
            continue
        value = nutrient.get("value")
        if value is not None:
            nutrients[key] = float(value)

    return {
        "description": best.get("description", query),
        "fdc_id": best.get("fdcId"),
        "nutrition": nutrients,
    }
