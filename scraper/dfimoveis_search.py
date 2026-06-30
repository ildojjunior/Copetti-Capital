import re
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_search_page(search_url: str):
    response = requests.get(search_url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def extract_listing_urls(search_url: str):
    """
    Extracts individual property listing URLs from a DFImóveis search page.
    """

    html = fetch_search_page(search_url)
    soup = BeautifulSoup(html, "html.parser")

    urls = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]

        if "/imovel/" in href:
            if href.startswith("/"):
                href = "https://www.dfimoveis.com.br" + href

            href = href.split("?")[0]

            if re.search(r"-\d+$", href):
                urls.add(href)

    return sorted(urls)