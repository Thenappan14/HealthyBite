from __future__ import annotations

import json
from typing import Any

from app.core.config import settings
from app.services.openai_analysis import get_openai_client


ENRICHMENT_BATCH_SIZE = 20


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

    enriched: list[dict[str, Any]] = []
    for start in range(0, len(items), ENRICHMENT_BATCH_SIZE):
        batch = items[start : start + ENRICHMENT_BATCH_SIZE]
        enriched.extend(_enrich_menu_item_batch(batch, start))
    return enriched


def _enrich_menu_item_batch(items: list[dict[str, Any]], offset: int) -> list[dict[str, Any]]:
    client = get_openai_client()
    indexed_items = [
        {
            "input_index": offset + idx,
            **item,
        }
        for idx, item in enumerate(items)
    ]

    response = client.responses.create(
        model=settings.openai_menu_model,
        instructions=(
            "You are a restaurant menu analysis assistant. Use only the provided menu item text and fields. "
            "Do not use external databases, web search, USDA data, or fixed nutrition tables. "
            "Return conservative estimates and keep confidence lower when details are sparse. "
            "Do not claim medical certainty. Preserve every input item exactly once."
        ),
        input=(
            "Enrich each menu item in the same order it is provided. Return the same number of items. "
            "Preserve category, name, description, price, source_page, and source_text from each original item. "
            "Add inferred ingredients, nutrition estimates, allergens, diet compatibility, and confidence score.\n\n"
            f"Menu items JSON:\n{json.dumps(indexed_items, ensure_ascii=True)}"
        ),
        temperature=0.3,
        timeout=45,
        text={
            "format": {
                "type": "json_schema",
                "name": "nutrition_enrichment",
                "schema": NUTRITION_ENRICHMENT_SCHEMA,
                "strict": True,
            }
        },
    )

    parsed = json.loads(response.output_text)
    enriched_items = parsed.get("items", [])
    if len(enriched_items) != len(items):
        return [_merge_fallback_item(item) for item in items]
    return [_merge_enriched_item(original, enriched) for original, enriched in zip(items, enriched_items)]


def _merge_enriched_item(original: dict[str, Any], enriched: dict[str, Any]) -> dict[str, Any]:
    return {
        **original,
        "category": original.get("category"),
        "name": original.get("name") or enriched.get("name") or "Unknown Dish",
        "description": original.get("description"),
        "price": original.get("price"),
        "source_page": original.get("source_page"),
        "source_text": original.get("source_text"),
        "inferred_ingredients": enriched.get("inferred_ingredients", []),
        "nutrition_estimate": enriched.get("nutrition_estimate") or _empty_nutrition_estimate(),
        "allergens": enriched.get("allergens", []),
        "diet_compatibility": enriched.get("diet_compatibility", []),
        "confidence_score": enriched.get("confidence_score", 0.4),
    }


def _merge_fallback_item(original: dict[str, Any]) -> dict[str, Any]:
    source_text = " ".join(
        str(part)
        for part in (original.get("name"), original.get("description"), original.get("source_text"))
        if part
    )
    return {
        **original,
        "inferred_ingredients": [],
        "nutrition_estimate": _empty_nutrition_estimate(),
        "allergens": _infer_common_allergens(source_text),
        "diet_compatibility": [],
        "confidence_score": 0.2,
    }


def _empty_nutrition_estimate() -> dict[str, float]:
    return {
        "calories": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "fiber_g": 0,
        "sugar_g": 0,
        "sodium_mg": 0,
    }


def _infer_common_allergens(text: str) -> list[str]:
    lowered = text.lower()
    allergens = {
        "peanut": "peanuts",
        "nut": "tree nuts",
        "almond": "tree nuts",
        "cashew": "tree nuts",
        "milk": "dairy",
        "cream": "dairy",
        "cheese": "dairy",
        "yogurt": "dairy",
        "egg": "eggs",
        "wheat": "gluten",
        "flour": "gluten",
        "soy": "soy",
        "prawn": "shellfish",
        "shrimp": "shellfish",
        "crab": "shellfish",
    }
    return sorted({label for token, label in allergens.items() if token in lowered})
