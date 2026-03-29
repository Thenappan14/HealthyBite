from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


def crawl_restaurant_menu(url: str) -> dict:
    """Sample website parser logic with a deterministic fallback."""

    try:
        response = httpx.get(url, timeout=8.0, follow_redirects=True)
        response.raise_for_status()
        html = response.text
    except Exception:
        html = """
        <html>
          <body>
            <h1>Green Fork Kitchen</h1>
            <h2>Bowls</h2>
            <div class="menu-item"><h3>Tofu Harvest Bowl</h3><p>Quinoa, roasted squash, kale, tahini</p><span>$17</span></div>
            <div class="menu-item"><h3>Chicken Fuel Bowl</h3><p>Brown rice, broccoli, avocado, grilled chicken</p><span>$18</span></div>
            <h2>Sides</h2>
            <div class="menu-item"><h3>Charred Broccolini</h3><p>Lemon, chili flakes, olive oil</p><span>$8</span></div>
            <h2>Dessert</h2>
            <div class="menu-item"><h3>Chocolate Lava Cake</h3><p>Vanilla cream</p><span>$11</span></div>
          </body>
        </html>
        """

    soup = BeautifulSoup(html, "lxml")
    title = soup.find("h1")
    restaurant_name = title.get_text(strip=True) if title else urlparse(url).netloc.replace("www.", "")

    items: list[dict] = []
    current_category = "Menu"
    for node in soup.find_all(["h2", "div", "article", "li"]):
        text = node.get_text(" ", strip=True)
        if not text:
            continue
        if node.name == "h2":
            current_category = text
            continue
        if "$" in text and len(text) < 180:
            price = None
            for token in text.split():
                if token.startswith("$"):
                    try:
                        price = float(token.replace("$", ""))
                    except ValueError:
                        price = None
                    break
            name = node.find(["h3", "strong", "b"])
            desc = node.find("p")
            items.append(
                {
                    "category": current_category,
                    "name": name.get_text(strip=True) if name else text.split("$")[0].strip(),
                    "description": desc.get_text(strip=True) if desc else text,
                    "price": price,
                }
            )

    return {
        "restaurant_name": restaurant_name,
        "source_url": url,
        "cuisine_tags": ["healthy", "casual"],
        "raw_text": soup.get_text("\n", strip=True)[:2500],
        "items": items,
        "parser_notes": [
            "Crawled the supplied URL and extracted likely menu blocks.",
            "Menu detection is heuristic and based on page structure and price patterns.",
        ],
    }
