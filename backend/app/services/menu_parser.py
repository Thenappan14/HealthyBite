def normalize_menu_text(text: str) -> dict:
    """Legacy compatibility shim.

    Menu normalization now happens through the OpenAI structured extraction pipeline.
    """

    return {"items": [], "parser_notes": [text] if text else []}
