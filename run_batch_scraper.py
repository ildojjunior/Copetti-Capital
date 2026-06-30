from scraper.batch_scraper import scrape_search_results

search_url = "https://www.dfimoveis.com.br/venda/df/brasilia/kitnet"

scrape_search_results(search_url, max_listings=3)