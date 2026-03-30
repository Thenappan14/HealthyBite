from __future__ import annotations

from typing import Any


INGREDIENT_HINTS = {
    "salmon": {"protein": 30, "fat": 18, "carbs": 12, "fiber": 4, "sugar": 4, "sodium": 520, "calories": 410, "allergens": ["fish"], "diets": ["pescatarian", "halal"]},
    "chicken": {"protein": 32, "fat": 14, "carbs": 16, "fiber": 3, "sugar": 4, "sodium": 620, "calories": 420, "allergens": [], "diets": ["halal"]},
    "tofu": {"protein": 20, "fat": 14, "carbs": 18, "fiber": 6, "sugar": 4, "sodium": 480, "calories": 350, "allergens": ["soy"], "diets": ["vegetarian", "vegan", "halal"]},
    "mushroom": {"protein": 12, "fat": 16, "carbs": 45, "fiber": 5, "sugar": 6, "sodium": 690, "calories": 460, "allergens": [], "diets": ["vegetarian"]},
    "steak": {"protein": 36, "fat": 25, "carbs": 32, "fiber": 2, "sugar": 3, "sodium": 780, "calories": 620, "allergens": [], "diets": ["halal"]},
    "yogurt": {"protein": 13, "fat": 8, "carbs": 30, "fiber": 4, "sugar": 20, "sodium": 180, "calories": 290, "allergens": ["dairy"], "diets": ["vegetarian", "gluten_free"]},
    "pasta": {"protein": 15, "fat": 20, "carbs": 68, "fiber": 5, "sugar": 7, "sodium": 720, "calories": 560, "allergens": ["gluten", "dairy"], "diets": ["vegetarian"]},
    "salad": {"protein": 10, "fat": 12, "carbs": 20, "fiber": 7, "sugar": 5, "sodium": 320, "calories": 260, "allergens": [], "diets": ["vegetarian", "vegan", "gluten_free", "halal", "pescatarian"]},
    "cake": {"protein": 6, "fat": 24, "carbs": 58, "fiber": 1, "sugar": 38, "sodium": 340, "calories": 520, "allergens": ["gluten", "dairy", "eggs"], "diets": ["vegetarian"]},
    "broccoli": {"protein": 8, "fat": 7, "carbs": 16, "fiber": 7, "sugar": 4, "sodium": 180, "calories": 160, "allergens": [], "diets": ["vegetarian", "vegan", "gluten_free", "halal", "pescatarian"]},
}

STRICT_DIETS = {
    "vegetarian": {"blocked_terms": ["chicken", "steak", "fish", "salmon", "beef", "pork"]},
    "vegan": {"blocked_terms": ["chicken", "steak", "fish", "salmon", "beef", "pork", "cheese", "cream", "yogurt", "butter", "egg", "parmesan"]},
    "halal": {"blocked_terms": ["pork", "bacon", "ham", "wine", "beer"]},
    "hindu_friendly": {"blocked_terms": ["beef"]},
    "buddhist_friendly": {"blocked_terms": ["beef", "pork", "chicken", "fish", "salmon", "shrimp", "prawn", "oyster"]},
    "no_beef": {"blocked_terms": ["beef"]},
    "no_pork": {"blocked_terms": ["pork", "bacon", "ham"]},
    "pescatarian": {"blocked_terms": ["chicken", "steak", "beef", "pork"]},
    "lactose_free": {"blocked_terms": ["cream", "milk", "cheese", "yogurt", "butter", "parmesan"]},
    "gluten_free": {"blocked_terms": ["pasta", "bread", "soy sauce", "flour", "wheat", "noodle"]},
}


def enrich_menu_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for item in items:
        merged_text = f"{item.get('name', '')} {item.get('description', '')}".lower()
        matched = [name for name in INGREDIENT_HINTS if name in merged_text]
        template = _combine_templates(matched)
        allergens = sorted(set(template["allergens"] + _keyword_allergens(merged_text)))
        diets = _compatible_diets(merged_text, template["diets"])
        confidence = round(min(0.95, 0.45 + 0.1 * len(matched)), 2)

        enriched.append(
            {
                **item,
                "inferred_ingredients": matched or _infer_ingredients(merged_text),
                "nutrition_estimate": {
                    "calories": template["calories"],
                    "protein_g": template["protein"],
                    "carbs_g": template["carbs"],
                    "fat_g": template["fat"],
                    "fiber_g": template["fiber"],
                    "sugar_g": template["sugar"],
                    "sodium_mg": template["sodium"],
                },
                "allergens": allergens,
                "diet_compatibility": diets,
                "confidence_score": confidence,
            }
        )
    return enriched


def _combine_templates(matched: list[str]) -> dict[str, Any]:
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
            "diets": ["none"],
        }

    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0,
    }
    allergens: list[str] = []
    diets: list[str] = []

    for key in matched:
        template = INGREDIENT_HINTS[key]
        for macro in totals:
            totals[macro] += template[macro]
        allergens.extend(template["allergens"])
        diets.extend(template["diets"])

    count = len(matched)
    averaged = {macro: round(value / count, 1) for macro, value in totals.items()}
    averaged["allergens"] = allergens
    averaged["diets"] = sorted(set(diets))
    return averaged


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
    candidates = ["rice", "greens", "tomato", "garlic", "avocado", "herbs"]
    return [item for item in candidates if item in text][:4] or ["mixed ingredients"]
