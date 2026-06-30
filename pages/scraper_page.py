import streamlit as st

from scraper.batch_scraper import scrape_search_results


def show_scraper_page():
    st.title("🌐 Market Scraper")
    st.write("Scrape DFImóveis search results and update the property database.")

    search_url = st.text_input(
        "DFImóveis Search URL",
        value="https://www.dfimoveis.com.br/venda/df/brasilia/kitnet",
    )

    max_listings = st.number_input(
        "Maximum listings to scrape",
        min_value=1,
        max_value=100,
        value=3,
        step=1,
    )

    if st.button("Scrape DFImóveis"):
        with st.spinner("Scraping DFImóveis..."):
            results = scrape_search_results(
                search_url,
                max_listings=int(max_listings),
            )

        st.success(f"Scraping finished. {len(results)} new listings inserted.")