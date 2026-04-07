from __future__ import annotations

import re
from typing import Any


PRICE_PATTERN = re.compile(r"(?P<currency>S?\$)?\s*(?P<price>\d{1,3}(?:\.\d{1,2})?)$")
CATEGORY_HINTS = {
    "starter",
    "starters",
    "appetizer",
    "appetizers",
    "mains",
    "main",
    "dessert",
    "desserts",
    "drinks",
    "beverages",
    "salads",
    "soups",
    "pasta",
    "pizza",
    "burgers",
    "seafood",
    "meat",
    "ice cream"
}


def normalize_menu_text(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = [line for line in lines if line]

    items: list[dict[str, Any]] = []
    parser_notes: list[str] = []
    current_category: str | None = None

    for idx, line in enumerate(cleaned_lines):
        normalized = re.sub(r"\s+", " ", line)
        if _is_category_line(normalized):
            current_category = normalized.title()
            continue

        price_match = PRICE_PATTERN.search(normalized)
        next_line = cleaned_lines[idx + 1] if idx + 1 < len(cleaned_lines) else ""

        if price_match or _looks_like_menu_item(normalized):
            item_line = normalized
            price = None
            if price_match:
                price = float(price_match.group("price"))
                item_line = normalized[: price_match.start()].strip(" -:")

            name, description = _split_name_description(item_line, next_line)
            if not name:
                continue

            items.append(
                {
                    "category": current_category,
                    "name": name,
                    "description": description,
                    "price": price
                }
            )

    if not items and cleaned_lines:
        parser_notes.append("Structured parsing was limited, so the menu text may need a cleaner upload.")
        items.extend(_fallback_chunk_items(cleaned_lines))

    if not parser_notes:
        parser_notes.append("Menu text was normalized with local rule-based parsing.")

    return {"items": items, "parser_notes": parser_notes}


def _is_category_line(line: str) -> bool:
    lowered = line.lower().strip(":")
    return lowered in CATEGORY_HINTS or (line.isupper() and len(line.split()) <= 4)


def _looks_like_menu_item(line: str) -> bool:
    tokens = line.split()
    if len(tokens) < 2:
        return False
    return any(char.isalpha() for char in line) and len(line) <= 120


def _split_name_description(line: str, next_line: str) -> tuple[str, str | None]:
    separators = [" - ", ":", " – ", " — "]
    for separator in separators:
        if separator in line:
            name, description = line.split(separator, 1)
            return name.strip().title(), description.strip() or None

    if next_line and len(next_line.split()) > 3 and not PRICE_PATTERN.search(next_line):
        return line.strip().title(), next_line.strip()

    return line.strip().title(), None


def _fallback_chunk_items(lines: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for chunk in lines[:10]:
        if len(chunk.split()) < 2:
            continue
        items.append(
            {
                "category": None,
                "name": chunk[:60].title(),
                "description": None,
                "price": None
            }
        )
    return items
