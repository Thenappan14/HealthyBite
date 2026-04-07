from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "ingredient_profiles.json"

STRICT_DIETS = {
    "vegetarian": {"blocked_terms": ["chicken", "steak", "fish", "salmon", "beef", "pork", "lamb", "duck", "shrimp", "prawn"]},
    "vegan": {"blocked_terms": ["chicken", "steak", "fish", "salmon", "beef", "pork", "lamb", "duck", "shrimp", "prawn", "cheese", "cream", "yogurt", "butter", "egg", "parmesan", "milk"]},
    "halal": {"blocked_terms": ["pork", "bacon", "ham", "wine", "beer"]},
    "hindu_friendly": {"blocked_terms": ["beef"]},
    "buddhist_friendly": {"blocked_terms": ["beef", "pork", "chicken", "fish", "salmon", "shrimp", "prawn", "oyster", "duck", "lamb"]},
    "no_beef": {"blocked_terms": ["beef"]},
    "no_pork": {"blocked_terms": ["pork", "bacon", "ham"]},
    "pescatarian": {"blocked_terms": ["chicken", "steak", "beef", "pork", "lamb", "duck"]},
    "lactose_free": {"blocked_terms": ["cream", "milk", "cheese", "yogurt", "butter", "parmesan"]},
    "gluten_free": {"blocked_terms": ["pasta", "bread", "soy sauce", "flour", "wheat", "noodle", "bun", "tempura"]}
}

PORTION_MODIFIERS = {
    "large": 1.35,
    "double": 1.45,
    "sharing": 1.6,
    "small": 0.8,
    "mini": 0.65,
    "light": 0.85
}

COOKING_ADJUSTMENTS = {
    "fried": {"calories": 1.22, "fat": 1.35, "sodium": 1.15},
    "crispy": {"calories": 1.18, "fat": 1.25, "sodium": 1.1},
    "tempura": {"calories": 1.18, "fat": 1.28, "sodium": 1.08},
    "grilled": {"calories": 0.96, "fat": 0.95, "sodium": 0.96},
    "steamed": {"calories": 0.9, "fat": 0.88, "sodium": 0.94},
    "roasted": {"calories": 1.02, "fat": 1.04, "sodium": 0.98},
    "creamy": {"calories": 1.16, "fat": 1.22, "sodium": 1.08},
    "cheesy": {"calories": 1.14, "fat": 1.18, "sodium": 1.12},
    "spicy": {"sodium": 1.05},
    "soup": {"sodium": 1.12}
}


def enrich_menu_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    ingredient_index = _ingredient_index()
    for item in items:
        merged_text = f"{item.get('name', '')} {item.get('description', '')}".lower()
        matched_profiles = _match_ingredient_profiles(merged_text, ingredient_index)
        template = _estimate_from_ingredients(matched_profiles, merged_text)
        allergens = sorted(set(template["allergens"] + _keyword_allergens(merged_text)))
        diets = _compatible_diets(merged_text, template["diets"])
        confidence = _estimate_confidence(matched_profiles, merged_text)

        enriched.append(
            {
                **item,
                "inferred_ingredients": [entry["name"] for entry in matched_profiles] or _infer_ingredients(merged_text),
                "nutrition_estimate": {
                    "calories": template["calories"],
                    "protein_g": template["protein"],
                    "carbs_g": template["carbs"],
                    "fat_g": template["fat"],
                    "fiber_g": template["fiber"],
                    "sugar_g": template["sugar"],
                    "sodium_mg": template["sodium"]
                },
                "allergens": allergens,
                "diet_compatibility": diets,
                "confidence_score": confidence
            }
        )
    return enriched


@lru_cache
def _ingredient_index() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return [{"name": name, **payload} for name, payload in raw.items()]


def _estimate_from_ingredients(matched: list[dict[str, Any]], text: str) -> dict[str, Any]:
    if not matched:
        return {
            "calories": 420,
            "protein": 18,
            "carbs": 36,
            "fat": 18,
            "fiber": 4,
            "sugar": 7,
            "sodium": 520,
            "allergens": [],
            "diets": ["none"]
        }

    totals = {
        "calories": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
        "fiber": 0.0,
        "sugar": 0.0,
        "sodium": 0.0
    }
    allergens: list[str] = []
    diets: list[str] = []

    for template in matched:
        for macro in totals:
            totals[macro] += float(template[macro])
        allergens.extend(template["allergens"])
        diets.extend(template["diets"])

    averaged = {macro: round(value / len(matched), 1) for macro, value in totals.items()}
    averaged = _apply_portion_adjustments(averaged, text)
    averaged = _apply_cooking_adjustments(averaged, text)
    averaged["allergens"] = allergens
    averaged["diets"] = sorted(set(diets))
    return averaged


def _match_ingredient_profiles(text: str, ingredient_index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matched: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in ingredient_index:
        for alias in entry.get("aliases", []):
            if alias in text and entry["name"] not in seen:
                matched.append(entry)
                seen.add(entry["name"])
                break
    return matched


def _apply_portion_adjustments(template: dict[str, float], text: str) -> dict[str, float]:
    multiplier = 1.0
    for token, value in PORTION_MODIFIERS.items():
        if token in text:
            multiplier = max(multiplier, value)
    return {macro: round(amount * multiplier, 1) for macro, amount in template.items()}


def _apply_cooking_adjustments(template: dict[str, float], text: str) -> dict[str, float]:
    adjusted = dict(template)
    for token, changes in COOKING_ADJUSTMENTS.items():
        if token in text:
            for macro, multiplier in changes.items():
                adjusted[macro] = round(adjusted[macro] * multiplier, 1)
    return adjusted


def _keyword_allergens(text: str) -> list[str]:
    mappings = {
        "peanut": "peanuts",
        "shrimp": "shellfish",
        "prawn": "shellfish",
        "sesame": "sesame",
        "egg": "eggs",
        "cheese": "dairy",
        "cream": "dairy",
        "soy": "soy",
        "parmesan": "dairy",
        "milk": "dairy",
        "nut": "tree nuts"
    }
    return [label for token, label in mappings.items() if token in text]


def _compatible_diets(text: str, default_diets: list[str]) -> list[str]:
    if not default_diets:
        default_diets = ["none"]
    compatible = {"none"}
    compatible.update(default_diets)

    for diet, rule in STRICT_DIETS.items():
        if not any(term in text for term in rule["blocked_terms"]):
            compatible.add(diet)

    return sorted(compatible)


def _infer_ingredients(text: str) -> list[str]:
    candidates = ["rice", "leafy_greens", "tomato", "sauce", "avocado", "vegetable_mix", "beans"]
    return [item for item in candidates if item.replace("_", " ") in text or item in text][:4] or ["mixed ingredients"]


def _estimate_confidence(matched: list[dict[str, Any]], text: str) -> float:
    base = 0.42
    if matched:
        base += min(0.35, 0.09 * len(matched))
    if any(token in text for token in ["with", "served", "includes", "topped", "sauce"]):
        base += 0.08
    if len(text.split()) > 10:
        base += 0.05
    return round(min(0.94, base), 2)
