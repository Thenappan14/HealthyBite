from __future__ import annotations

from typing import Any

from app.models import MenuItemModel, UserProfileModel
from app.services.nutrition import STRICT_DIETS

DISCLAIMER = (
    "Recommendations are based on estimated nutrition and provided profile information. "
    "This is not medical advice."
)


def build_profile_model(profile: dict[str, Any]) -> UserProfileModel:
    return UserProfileModel(**profile)


def build_menu_item_models(items: list[dict[str, Any]]) -> list[MenuItemModel]:
    return [MenuItemModel(**item) for item in items]


def generate_recommendations(
    profile: UserProfileModel, items: list[MenuItemModel]
) -> dict[str, Any]:
    scored = []
    avoided = []

    for item in items:
        evaluation = score_item(profile, item)
        if evaluation["excluded"]:
            avoided.append(_serialize(item, evaluation, "avoid"))
        else:
            scored.append(_serialize(item, evaluation, "top_pick"))

    scored.sort(key=lambda entry: entry["match_score"], reverse=True)
    top = scored[:3]
    alternatives = [{**entry, "recommendation_type": "alternative"} for entry in scored[3:5]]
    avoid_candidates = avoided + [
        {**entry, "recommendation_type": "avoid"}
        for entry in sorted(scored[-2:], key=lambda current: current["match_score"])
    ]

    return {
        "disclaimer": DISCLAIMER,
        "top_recommendations": top,
        "alternatives": alternatives,
        "dishes_to_avoid": avoid_candidates[:3],
    }


def score_item(profile: UserProfileModel, item: MenuItemModel) -> dict[str, Any]:
    nutrition = item.nutrition_estimate or {}
    text = f"{item.name} {item.description or ''}".lower()
    reasons: list[str] = []
    downsides: list[str] = []
    warnings: list[str] = []
    score = 50.0

    allergies = {entry.lower() for entry in profile.allergies}
    item_allergens = {entry.lower() for entry in item.allergens}
    if allergies & item_allergens:
        return {
            "excluded": True,
            "score": 0.0,
            "reasons": [],
            "downsides": [f"Contains allergen risk: {', '.join(sorted(allergies & item_allergens))}."],
            "warnings": ["Excluded because the menu information suggests a direct allergy conflict."],
            "summary_reason": "Excluded due to likely allergen conflict.",
        }

    if profile.diet_type in STRICT_DIETS:
        blocked_terms = STRICT_DIETS[profile.diet_type]["blocked_terms"]
        if any(term in text for term in blocked_terms):
            return {
                "excluded": True,
                "score": 5.0,
                "reasons": [],
                "downsides": [f"Does not appear compatible with a {profile.diet_type} diet."],
                "warnings": ["Excluded based on likely ingredients from the menu wording."],
                "summary_reason": f"Excluded for {profile.diet_type} compatibility.",
            }

    goal_bonus, goal_reason = _goal_alignment(profile.primary_goal, nutrition)
    score += goal_bonus
    reasons.append(goal_reason)

    protein = float(nutrition.get("protein_g", 0))
    calories = float(nutrition.get("calories", 0))
    sugar = float(nutrition.get("sugar_g", 0))
    sodium = float(nutrition.get("sodium_mg", 0))
    fiber = float(nutrition.get("fiber_g", 0))

    if protein >= 25:
        score += 10
        reasons.append("Provides a likely solid protein serving.")
    elif protein < 12:
        score -= 6
        downsides.append("Protein looks relatively low.")

    if 300 <= calories <= 650:
        score += 8
        reasons.append("Estimated calories are in a practical meal range.")
    else:
        score -= 4
        downsides.append("Estimated calories may be less aligned with an everyday meal target.")

    if sugar > 20:
        score -= 8
        downsides.append("Estimated sugar is on the higher side.")
    if sodium > 800:
        score -= 7
        downsides.append("Estimated sodium is relatively high.")
    if fiber >= 6:
        score += 6
        reasons.append("Includes a likely fiber benefit.")

    if any(token in text for token in ["salad", "greens", "broccoli", "kale", "vegetable", "avocado"]):
        score += 5
        reasons.append("Menu wording suggests vegetables or nutrient-dense sides.")

    if any(cuisine.lower() in text for cuisine in profile.preferred_cuisines):
        score += 4
        reasons.append("Matches a preferred cuisine signal from the profile.")

    price = float(item.price or 0)
    if profile.budget_preference == "budget" and price and price > 18:
        score -= 5
        downsides.append("Price looks above the stated budget preference.")
    elif profile.budget_preference == "flexible" or (price and price <= 18):
        score += 3
        reasons.append("Price is reasonably aligned with the budget setting.")

    if any(disliked.lower() in text for disliked in profile.disliked_foods):
        score -= 6
        downsides.append("Includes ingredients the user has marked as disliked.")

    confidence_weight = float(item.confidence_score or 0.5)
    if confidence_weight < 0.55:
        warnings.append(
            "Nutrition estimate confidence is lower because ingredients were inferred from limited menu text."
        )
    score *= 0.75 + 0.25 * confidence_weight

    if item.allergens:
        warnings.append("Contains possible allergens based on likely ingredients and menu wording.")

    summary = reasons[0] if reasons else "Estimated as a moderate fit based on menu information."
    return {
        "excluded": False,
        "score": round(max(0, min(score, 100)), 1),
        "reasons": reasons[:4],
        "downsides": downsides[:3],
        "warnings": warnings[:3],
        "summary_reason": summary,
    }


def _goal_alignment(goal: str, nutrition: dict[str, Any]) -> tuple[int, str]:
    protein = float(nutrition.get("protein_g", 0))
    calories = float(nutrition.get("calories", 0))
    fiber = float(nutrition.get("fiber_g", 0))

    if goal == "fat_loss":
        if calories <= 550 and protein >= 20:
            return 14, "Supports fat-loss goals with a likely favorable calorie-to-protein balance."
        return 4, "Has some fat-loss potential based on estimated portion size."
    if goal == "muscle_gain":
        if protein >= 28 and calories >= 450:
            return 14, "Supports muscle-gain goals with likely stronger protein and energy intake."
        return 5, "Offers some muscle-gain support but may be lighter than ideal."
    if goal == "better_energy":
        if calories >= 350 and fiber >= 5:
            return 12, "Looks supportive for steady energy with likely fiber and meal substance."
        return 5, "May offer moderate energy support."
    if goal == "balanced_eating":
        if 350 <= calories <= 650 and fiber >= 4:
            return 12, "Fits balanced-eating goals with a likely well-rounded nutrition profile."
        return 6, "Appears reasonably balanced from menu information."
    return 8, "Estimated as generally appropriate for maintenance."


def _serialize(
    item: MenuItemModel, evaluation: dict[str, Any], recommendation_type: str
) -> dict[str, Any]:
    return {
        "menu_item_id": item.id,
        "dish_name": item.name,
        "category": item.category,
        "match_score": evaluation["score"],
        "summary_reason": evaluation["summary_reason"],
        "nutrition_estimate": item.nutrition_estimate,
        "allergens": item.allergens,
        "warnings": evaluation["warnings"],
        "why_recommended": evaluation["reasons"],
        "why_not_recommended": evaluation["downsides"],
        "recommendation_type": recommendation_type,
    }
