def extract_text_from_upload(filename: str, content: bytes) -> str:
    """Legacy placeholder retained for compatibility.

    The main upload analysis path now uses OpenAI multimodal file/image inputs directly.
    """

    try:
        decoded = content.decode("utf-8")
        return decoded.strip()
    except UnicodeDecodeError:
        return f"Binary upload received for {filename}."
