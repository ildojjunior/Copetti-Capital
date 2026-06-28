import re
import requests
from bs4 import BeautifulSoup


def extract_listing_id(url: str) -> str:
    match = re.search(r"-(\d+)$", url)
    if match:
        return match.group(1)
    return ""


def clean_number(value: str):
    if not value:
        return None

    value = value.strip()
    value = value.replace(".", "")
    value = value.replace(",", ".")
    value = re.sub(r"[^\d.]", "", value)

    if value == "":
        return None

    return float(value)


def fetch_page(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    return response.text


def parse_price(soup: BeautifulSoup):
    price_tag = soup.find(attrs={"itemprop": "price"})

    if price_tag:
        content_price = price_tag.get("content")
        if content_price:
            return clean_number(content_price)

        visible_price = price_tag.get_text(strip=True)
        return clean_number(visible_price)

    return None

def parse_area(soup: BeautifulSoup):
    area_tag = soup.find(attrs={"itemprop": "floorSize"})

    if area_tag:
        area_text = area_tag.get_text(strip=True)
        return clean_number(area_text)

    return None


def parse_dfimoveis_listing(url: str) -> dict:
    html = fetch_page(url)
    soup = BeautifulSoup(html, "lxml")

    page_title = soup.title.get_text(strip=True) if soup.title else ""

    return {
        "source": "DFImóveis",
        "listing_url": url,
        "listing_id": extract_listing_id(url),
        "page_title": page_title,
        "asking_price": parse_price(soup),
        "area_m2": parse_area(soup),
        "html_length": len(html),
    }