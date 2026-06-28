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

def parse_data_attribute(soup: BeautifulSoup, attribute_name: str):
    tag = soup.find(attrs={attribute_name: True})

    if tag:
        return tag.get(attribute_name)

    return None

def parse_condo_fee(html: str):
    match = re.search(r"Condomínio\s*<br\s*/?>\s*R\$\s*([\d.,]+)", html)

    if match:
        return clean_number(match.group(1))

    return None

def calculate_price_per_m2(asking_price, area_m2):
    if asking_price and area_m2 and area_m2 > 0:
        return round(asking_price / area_m2, 2)

    return None

def parse_iptu(html: str):
    match = re.search(
        r"IPTU R\$:\s*<span[^>]*>\s*([\d.,]+)\s*</span>",
        html
    )

    if match:
        return clean_number(match.group(1))

    return None

def parse_floor(html: str):
    match = re.search(
        r"Andar do Apartamento:\s*<span[^>]*>\s*(\d+)",
        html
    )

    if match:
        return int(match.group(1))

    return None

def parse_list_text_field(html: str, label: str):
    pattern = rf"{label}:\s*<span[^>]*>\s*([^<]+)\s*</span>"
    match = re.search(pattern, html)

    if match:
        return match.group(1).strip()

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
        "iptu": parse_iptu(html),
        "condo_fee": parse_condo_fee(html),
        "area_m2": parse_area(soup),
        "price_per_m2": calculate_price_per_m2(parse_price(soup), parse_area(soup)),
        "floor": parse_floor(html),
        "bedrooms": clean_number(parse_data_attribute(soup, "data-quartos")),
        "property_type": parse_data_attribute(soup, "data-tipo"),
        "property_subtype": parse_data_attribute(soup, "data-subtipo"),
        "transaction_type": parse_data_attribute(soup, "data-negocio"),
        "solar_orientation": parse_list_text_field(html, "Posição do Sol"),
        "property_position": parse_list_text_field(html, "Posição do Imóvel"),
        "neighborhood": parse_data_attribute(soup, "data-bairro"),
        "cep_partial": parse_data_attribute(soup, "data-cepparcial"),
        "city": parse_data_attribute(soup, "data-cidade"),
        "uf": parse_data_attribute(soup, "data-uf"),
        "html_length": len(html),
    }