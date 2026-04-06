import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    organization = os.environ.get("OPENAI_ORGANIZATION")
    project = os.environ.get("OPENAI_PROJECT")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in backend/.env")

    client = OpenAI(
        api_key=api_key,
        organization=organization,
        project=project,
    )
    endpoint = "/v1/responses"
    model = "gpt-4o-mini"
    timestamp_utc = datetime.now(timezone.utc).isoformat()

    print("UTC timestamp:", timestamp_utc)
    print("Endpoint:", endpoint)
    print("Model:", model)
    print("Organization:", organization)
    print("Project:", project)

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
