def extract_text_from_upload(filename: str, content: bytes) -> str:
    """Placeholder OCR extractor.

    In production this service would call an OCR engine such as Tesseract or a vision model.
    For the scaffold, we treat text-heavy files as UTF-8 when possible and otherwise return
    a representative menu transcript so downstream parsing remains testable.
    """

    try:
        decoded = content.decode("utf-8")
        if decoded.strip():
            return decoded
    except UnicodeDecodeError:
        pass

    return f"""
    Sample OCR extraction for {filename}
    Starters
    Grilled Halloumi Salad - mixed greens, cherry tomato, lemon herb dressing - $12
    Crispy Chicken Lettuce Wraps - peanut sauce, cabbage slaw - $14

    Mains
    Salmon Power Bowl - brown rice, kale, avocado, edamame, sesame dressing - $21
    Truffle Mushroom Pasta - cream sauce, parmesan, garlic - $19
    Steak Frites - sirloin steak, fries, herb butter - $28

    Desserts
    Greek Yogurt Berry Parfait - granola, berries, honey - $9
    """

