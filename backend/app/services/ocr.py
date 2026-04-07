from __future__ import annotations

import io
from pathlib import Path

from pypdf import PdfReader

try:
    from pdf2image import convert_from_bytes
    import pytesseract
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency path
    convert_from_bytes = None
    pytesseract = None
    Image = None


def extract_text_from_upload(filename: str, content: bytes) -> str:
    document = extract_document_payload(filename, content)
    return document["text"]


def extract_document_payload(filename: str, content: bytes) -> dict:
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf_document(content)

    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        text = _extract_image_text(content, filename)
        return {"text": text, "pages": [{"page_number": 1, "text": text}]}

    try:
        text = content.decode("utf-8").strip()
        return {"text": text, "pages": [{"page_number": 1, "text": text}] if text else []}
    except UnicodeDecodeError:
        return {"text": "", "pages": []}


def _extract_pdf_document(content: bytes) -> dict:
    reader = PdfReader(io.BytesIO(content))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        extracted = (page.extract_text() or "").strip()
        if extracted:
            pages.append({"page_number": index, "text": extracted})

    extracted = "\n\n".join(page["text"] for page in pages)
    if extracted:
        return {"text": extracted, "pages": pages}
    return _extract_scanned_pdf_document(content)


def _extract_image_text(content: bytes, filename: str) -> str:
    if pytesseract is None or Image is None:
        raise RuntimeError(
            "Image OCR requires pytesseract and Pillow. Install dependencies and make sure Tesseract OCR is available."
        )

    image = Image.open(io.BytesIO(content))
    text = pytesseract.image_to_string(image)
    if not text.strip():
        raise RuntimeError(
            f"No readable text was found in {filename}. Try a clearer photo or higher-resolution screenshot."
        )
    return text.strip()


def _extract_scanned_pdf_document(content: bytes) -> dict:
    if convert_from_bytes is None or pytesseract is None:
        raise RuntimeError(
            "Scanned PDF OCR requires pdf2image, pytesseract, and a local Poppler install."
        )

    try:
        images = convert_from_bytes(content, dpi=250)
    except Exception as exc:
        raise RuntimeError(
            "Scanned PDF conversion failed. Install Poppler on Windows or try uploading screenshots instead."
        ) from exc

    page_text = []
    pages = []
    for index, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image).strip()
        if text:
            page_text.append(text)
            pages.append({"page_number": index, "text": text})

    extracted = "\n\n".join(page_text)
    if not extracted:
        raise RuntimeError(
            "No readable text was found in the scanned PDF. Try clearer screenshots or a higher-quality scan."
        )
    return {"text": extracted, "pages": pages}
