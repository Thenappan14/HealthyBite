import re


def normalize_menu_text(text: str) -> dict:
    items: list[dict] = []
    current_category = "Uncategorized"
    line_pattern = re.compile(
        r"^(?P<name>[^-]+?)\s*-\s*(?P<description>.+?)\s*-\s*\$(?P<price>\d+(?:\.\d+)?)$"
    )

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "-" not in line and "$" not in line and len(line.split()) <= 3:
            current_category = line
            continue

        match = line_pattern.match(line)
        if match:
            items.append(
                {
                    "category": current_category,
                    "name": match.group("name").strip(),
                    "description": match.group("description").strip(),
                    "price": float(match.group("price")),
                }
            )
        else:
            items.append(
                {
                    "category": current_category,
                    "name": line[:60],
                    "description": "Estimated from OCR text with partial structure.",
                    "price": None,
                }
            )

    return {"items": items, "parser_notes": ["Normalized from OCR text with rule-based parsing."]}

