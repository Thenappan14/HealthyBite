from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


def crawl_restaurant_menu(url: str) -> dict:
    """Fetch website context for downstream LLM-based menu extraction."""

    response = httpx.get(url, timeout=10.0, follow_redirects=True)
    response.raise_for_status()
    html = response.text

    soup = BeautifulSoup(html, "lxml")
    title = soup.find("h1")
    restaurant_name = title.get_text(strip=True) if title else urlparse(url).netloc.replace("www.", "")

    return {
        "restaurant_name": restaurant_name,
        "source_url": url,
        "raw_text": soup.get_text("\n", strip=True)[:2500],
        "html_excerpt": html[:12000],
        "parser_notes": [
            "Fetched the supplied URL for downstream LLM-based menu extraction.",
        ],
    }
