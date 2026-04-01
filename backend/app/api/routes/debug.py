from fastapi import APIRouter
from openai import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError

from app.core.config import settings
from app.services.openai_analysis import get_openai_client

router = APIRouter()


@router.get("/openai-test")
def openai_test() -> dict:
    masked_key = None
    if settings.openai_api_key:
        masked_key = f"...{settings.openai_api_key[-6:]}"

    try:
        client = get_openai_client()
        response = client.responses.create(
            model=settings.openai_menu_model,
            input="Reply with exactly OK",
        )
        return {
            "ok": True,
            "model": settings.openai_menu_model,
            "key_suffix": masked_key,
            "output": response.output_text,
        }
    except RateLimitError:
        return {
            "ok": False,
            "model": settings.openai_menu_model,
            "key_suffix": masked_key,
            "error_type": "rate_limit",
            "detail": "OpenAI quota exceeded for the key currently loaded by the backend.",
        }
    except AuthenticationError:
        return {
            "ok": False,
            "model": settings.openai_menu_model,
            "key_suffix": masked_key,
            "error_type": "auth",
            "detail": "OpenAI authentication failed for the key currently loaded by the backend.",
        }
    except APIConnectionError:
        return {
            "ok": False,
            "model": settings.openai_menu_model,
            "key_suffix": masked_key,
            "error_type": "connection",
            "detail": "The backend could not connect to OpenAI.",
        }
    except APIStatusError as exc:
        return {
            "ok": False,
            "model": settings.openai_menu_model,
            "key_suffix": masked_key,
            "error_type": "api_status",
            "detail": f"OpenAI API returned status {exc.status_code}.",
        }
    except RuntimeError as exc:
        return {
            "ok": False,
            "model": settings.openai_menu_model,
            "key_suffix": masked_key,
            "error_type": "runtime",
            "detail": str(exc),
        }

