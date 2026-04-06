from __future__ import annotations

import base64
import io
import json
from typing import Any

from openai import OpenAI
from pypdf import PdfReader

from app.core.config import settings


MENU_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "restaurant_name": {"type": "string"},
        "source_summary": {"type": "string"},
        "cuisine_tags": {"type": "array", "items": {"type": "string"}},
        "parser_notes": {"type": "array", "items": {"type": "string"}},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "price": {"type": ["number", "null"]},
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
                    "inferred_ingredients",
                    "nutrition_estimate",
                    "allergens",
                    "diet_compatibility",
                    "confidence_score",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": ["restaurant_name", "source_summary", "cuisine_tags", "parser_notes", "items"],
    "additionalProperties": False,
}

RECOMMENDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "disclaimer": {"type": "string"},
        "top_recommendations": {"$ref": "#/$defs/recommendation_list"},
        "alternatives": {"$ref": "#/$defs/recommendation_list"},
        "dishes_to_avoid": {"$ref": "#/$defs/recommendation_list"},
    },
    "$defs": {
        "recommendation_list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "menu_item_id": {"type": "integer"},
                    "dish_name": {"type": "string"},
                    "category": {"type": ["string", "null"]},
                    "match_score": {"type": "number"},
                    "summary_reason": {"type": "string"},
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
                    "warnings": {"type": "array", "items": {"type": "string"}},
                    "why_recommended": {"type": "array", "items": {"type": "string"}},
                    "why_not_recommended": {"type": "array", "items": {"type": "string"}},
                    "recommendation_type": {"type": "string"},
                },
                "required": [
                    "menu_item_id",
                    "dish_name",
                    "category",
                    "match_score",
                    "summary_reason",
                    "nutrition_estimate",
                    "allergens",
                    "warnings",
                    "why_recommended",
                    "why_not_recommended",
                    "recommendation_type",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["disclaimer", "top_recommendations", "alternatives", "dishes_to_avoid"],
    "additionalProperties": False,
}


def get_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to backend/.env before running AI analysis."
        )
    return OpenAI(
        api_key=settings.openai_api_key,
        organization=settings.openai_organization,
        project=settings.openai_project,
    )


def analyze_uploaded_menu(filename: str, content: bytes) -> dict[str, Any]:
    client = get_openai_client()
    prompt = (
        "You are a restaurant menu analysis assistant. Extract the menu into structured JSON. "
        "Infer likely ingredients and estimate nutrition conservatively from the menu information. "
        "Do not claim medical certainty. Use words like estimated, likely, and based on menu information."
    )

    suffix = filename.lower()
    user_content: list[dict[str, Any]] = []
    if suffix.endswith(".pdf"):
        extracted_text = _extract_pdf_text(content)
        user_content.append(
            {
                "type": "input_text",
                "text": (
                    f"Uploaded PDF filename: {filename}\n\n"
                    "Below is extracted PDF text from a restaurant menu. "
                    "Use only this menu information and make conservative estimates.\n\n"
                    f"{extracted_text[:18000]}"
                ),
            }
        )
    else:
        mime_type = _detect_image_mime_type(suffix)
        file_data = base64.b64encode(content).decode("utf-8")
        user_content.append(
            {
                "type": "input_image",
                "image_url": f"data:{mime_type};base64,{file_data}",
            }
        )

    user_content.append(
        {
            "type": "input_text",
            "text": (
                "Extract restaurant name if visible, menu items, categories, descriptions, prices, likely ingredients, "
                "estimated nutrition, allergens, diet compatibility, and a confidence score for each item."
            ),
        }
    )

    response = client.responses.create(
        model=settings.openai_menu_model,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "menu_analysis",
                "strict": True,
                "schema": MENU_ANALYSIS_SCHEMA,
            }
        },
    )
    return json.loads(response.output_text)


def analyze_restaurant_url(url: str, website_text: str) -> dict[str, Any]:
    client = get_openai_client()
    user_text = (
        f"Restaurant URL: {url}\n\n"
        "Below is scraped website text. Extract the menu into structured JSON. "
        "If the text is incomplete, make careful estimates and note uncertainty.\n\n"
        f"{website_text[:12000]}"
    )

    response = client.responses.create(
        model=settings.openai_menu_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a restaurant menu extraction assistant. Convert website content into structured menu data. "
                    "Estimate missing descriptions or nutrition only when necessary and mark uncertainty via confidence."
                ),
            },
            {"role": "user", "content": user_text},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "menu_analysis",
                "strict": True,
                "schema": MENU_ANALYSIS_SCHEMA,
            }
        },
    )
    parsed = json.loads(response.output_text)
    parsed["source_url"] = url
    return parsed


def generate_ai_recommendations(profile: dict[str, Any], menu_items: list[dict[str, Any]]) -> dict[str, Any]:
    client = get_openai_client()
    request_payload: dict[str, Any] = {
        "model": settings.openai_recommendation_model,
        "input": [
            {
                "role": "system",
                "content": (
                    "You are a nutrition guidance assistant for restaurant decisions, not a doctor. "
                    "Use the user's profile and menu item data to rank dishes. "
                    "Exclude allergy conflicts and strict diet conflicts. "
                    "If needed, you may use web search to sanity-check likely nutrition or ingredient details, "
                    "but do not fabricate medical certainty. "
                    "Always keep the disclaimer that this is not medical advice."
                ),
            },
            {
                "role": "user",
                "content": (
                    "User profile JSON:\n"
                    f"{json.dumps(profile, ensure_ascii=True)}\n\n"
                    "Menu items JSON:\n"
                    f"{json.dumps(menu_items, ensure_ascii=True)}"
                ),
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "recommendation_result",
                "strict": True,
                "schema": RECOMMENDATION_SCHEMA,
            }
        },
    }

    if settings.openai_enable_web_search:
        request_payload["tools"] = [{"type": "web_search_preview"}]

    response = client.responses.create(**request_payload)
    parsed = json.loads(response.output_text)
    return parsed


def _detect_image_mime_type(filename: str) -> str:
    if filename.endswith(".png"):
        return "image/png"
    if filename.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"


def _extract_pdf_text(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:
        raise RuntimeError(
            "The PDF could not be read locally before AI analysis. Try a text-based PDF or a clearer image."
        ) from exc

    extracted = "\n\n".join(page.strip() for page in pages if page and page.strip())
    if not extracted:
        raise RuntimeError(
            "No readable text was found in the PDF. Try a clearer PDF or upload screenshots instead."
        )
    return extracted
