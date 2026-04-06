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
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf_text(content)

    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        return _extract_image_text(content, filename)

    try:
        return content.decode("utf-8").strip()
    except UnicodeDecodeError:
        return ""


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    extracted = "\n\n".join(page.strip() for page in pages if page and page.strip())
    if extracted:
        return extracted
    return _extract_scanned_pdf_text(content)


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


def _extract_scanned_pdf_text(content: bytes) -> str:
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
    for image in images:
        text = pytesseract.image_to_string(image).strip()
        if text:
            page_text.append(text)

    extracted = "\n\n".join(page_text)
    if not extracted:
        raise RuntimeError(
            "No readable text was found in the scanned PDF. Try clearer screenshots or a higher-quality scan."
        )
    return extracted
