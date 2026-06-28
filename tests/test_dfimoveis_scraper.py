from scraper.dfimoveis import parse_dfimoveis_listing

url = "https://www.dfimoveis.com.br/imovel/kitnet-1-quarto-venda-asa-norte-brasilia-df-cln-213-1358762"

result = parse_dfimoveis_listing(url)

print(result)
