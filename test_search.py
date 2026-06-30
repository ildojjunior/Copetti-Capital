from scraper.dfimoveis_search import extract_listing_urls

url = "https://www.dfimoveis.com.br/venda/df/brasilia/kitnet"

urls = extract_listing_urls(url)

print(f"Found {len(urls)} listings\n")

for u in urls[:20]:
    print(u)