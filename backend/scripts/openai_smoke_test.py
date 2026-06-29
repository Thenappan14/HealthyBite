from datetime import datetime, timezone
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from openai import APIStatusError, OpenAI

from app.core.config import settings


def main() -> None:
    api_key = settings.openai_api_key
    organization = settings.openai_organization
    project = settings.openai_project
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in backend/.env")

    client = OpenAI(
        api_key=api_key,
        organization=organization,
        project=project,
    )
    endpoint = "/v1/responses"
    model = settings.openai_recommendation_model
    timestamp_utc = datetime.now(timezone.utc).isoformat()

    print("UTC timestamp:", timestamp_utc)
    print("Endpoint:", endpoint)
    print("Model:", model)
    print("API key loaded:", bool(api_key))
    print("Organization set:", bool(organization))
    print("Project set:", bool(project))

    try:
        response = client.responses.create(
            model=model,
            input="What is the capital of France? Reply in one short sentence.",
        )
        print("Output:", response.output_text)
    except APIStatusError as exc:
        print("Status:", exc.status_code)
        print("x-request-id:", exc.response.headers.get("x-request-id"))
        print("Body:", exc.response.text)
        raise


if __name__ == "__main__":
    main()
