import time

from database.db_utils import save_analyzed_property
from scraper.dfimoveis import parse_dfimoveis_listing
from scraper.dfimoveis_search import extract_listing_urls


def scrape_search_results(search_url: str, max_listings: int = 3):
    """
    Scrapes a small number of listings from a DFImóveis search page.
    """

    urls = extract_listing_urls(search_url)

    print(f"Found {len(urls)} listing URLs.")
    print(f"Scraping first {max_listings} listings.\n")

    results = []

    for url in urls[:max_listings]:
        print(f"Scraping: {url}")

        try:
            result = parse_dfimoveis_listing(url)
            saved = save_analyzed_property(result)
            if saved:
                results.append(result)
                print(f"Saved listing {result.get('listing_id')}")
            else:
                print(f"Skipped listing {result.get('listing_id')}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

        time.sleep(2)

    return results