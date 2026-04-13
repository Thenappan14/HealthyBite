from __future__ import annotations

import json
from typing import Any

from app.core.config import settings
from app.services.openai_analysis import get_openai_client


NUTRITION_ENRICHMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": ["string", "null"]},
                    "name": {"type": "string"},
                    "description": {"type": ["string", "null"]},
                    "price": {"type": ["number", "null"]},
                    "source_page": {"type": ["integer", "null"]},
                    "source_text": {"type": ["string", "null"]},
                    "inferred_ingredients": {"type": "array", "items": {"type": "string"}},
                    "nutrition_estimate": {
                        "type": "object",
                        "properties": {
                            "calories": {"type": "number"},
                            "protein_g": {"type": "number"},
                            "carbs_g": {"type": "number"},
                            "fat_g": {"type": "number"},
                            "fiber_g": {"type": "number"},
                            "sugar_g": {"type": "number"},
                            "sodium_mg": {"type": "number"},
                        },
                        "required": [
                            "calories",
                            "protein_g",
                            "carbs_g",
                            "fat_g",
                            "fiber_g",
                            "sugar_g",
                            "sodium_mg",
                        ],
                        "additionalProperties": False,
                    },
                    "allergens": {"type": "array", "items": {"type": "string"}},
                    "diet_compatibility": {"type": "array", "items": {"type": "string"}},
                    "confidence_score": {"type": "number"},
                },
                "required": [
                    "category",
                    "name",
                    "description",
                    "price",
                    "source_page",
                    "source_text",
                    "inferred_ingredients",
                    "nutrition_estimate",
                    "allergens",
                    "diet_compatibility",
                    "confidence_score",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


def enrich_menu_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not items:
        return []

    client = get_openai_client()
    response = client.chat.completions.create(
        model=settings.openai_menu_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a restaurant menu analysis assistant. Use only the provided menu item text and fields. "
                    "Do not use external databases, web search, USDA data, or fixed nutrition tables. "
                    "Return conservative estimates and keep confidence lower when details are sparse. "
                    "Do not claim medical certainty. "
                    "Always respond with valid JSON only, no additional text."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Enrich each menu item in the same order it is provided. Return the same number of items, "
                    "preserving the original fields while adding inferred ingredients, nutrition estimates, allergens, "
                    "diet compatibility, and a confidence score. "
                    "Return your response as a JSON object with an 'items' array.\n\n"
                    f"Menu items JSON:\n{json.dumps(items, ensure_ascii=True)}"
                ),
            },
        ],
        temperature=0.3,
    )

    parsed = json.loads(response.choices[0].message.content)
    enriched_items = parsed.get("items", [])
    if len(enriched_items) != len(items):
        raise RuntimeError("OpenAI returned a different number of enriched items than were provided.")
    return enriched_items
