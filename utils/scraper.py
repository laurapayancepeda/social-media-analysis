import requests
from bs4 import BeautifulSoup


def scrape_post(url: str) -> str:
    """Scrape main post text from a webpage"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        post_text = " ".join([p.get_text() for p in paragraphs])

        return post_text.strip()

    except Exception as e:
        return f"Error scraping {url}: {e}"
