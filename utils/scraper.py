# utils/scraper.py
import requests
from bs4 import BeautifulSoup


def scrape_post(url: str) -> str:
    """Scrape main post text from URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # Grab all <p> text
        post_text = " ".join([p.get_text() for p in soup.find_all("p")])
        return post_text.strip()
    except Exception as e:
        return f"Error scraping {url}: {e}"
