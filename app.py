import streamlit as st
from PIL import Image
from pathlib import Path

from valuation.valuation_engine import evaluate_property
from database.db_utils import get_dashboard_metrics, save_analyzed_property
from scraper.dfimoveis import parse_dfimoveis_listing
from valuation.market_intelligence import get_market_benchmarks

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Copetti Capital",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Load Logo
# -----------------------------
logo_path = Path("assets/logo.png")

if logo_path.exists():
    logo = Image.open(logo_path)
else:
    logo = None


# -----------------------------
# Sidebar
# -----------------------------
if logo:
    st.sidebar.image(logo, use_container_width=True)

st.sidebar.markdown("### Copetti Capital")
st.sidebar.markdown("*Investir. Analisar. Gerar Valor.*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔍 Property Analyzer",
        "🗄️ Database",
        "📊 Market Intelligence",
        "🗺️ Map",
        "💼 Portfolio",
    ],
)

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "🏠 Dashboard":

    st.title("🏠 Dashboard")
    st.subheader("Real Estate Investment Intelligence")

    metrics = get_dashboard_metrics()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Properties", metrics["total_properties"])
    c2.metric("BUY", metrics["buy_count"])
    c3.metric("NEGOTIATE", metrics["negotiate_count"])
    c4.metric("PASS", metrics["pass_count"])

    st.divider()

    st.header("Today's Market")
    st.info("No market scan has been performed yet.")


# -----------------------------
# PROPERTY ANALYZER
# -----------------------------
elif page == "🔍 Property Analyzer":

    st.title("🔍 Property Analyzer")
    st.write("Paste a DFImóveis or Wimoveis property URL.")

    property_url = st.text_input("Property URL")

    if st.button("Analyze Property"):

        if property_url:

            with st.spinner("Analyzing property..."):
                result = parse_dfimoveis_listing(property_url)
                result = evaluate_property(result)

            st.success("Property analyzed successfully!")

            save_analyzed_property(result)
            st.info("Property saved to database.")

            st.subheader("Extracted Property Data")

            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

            listing_id = result.get("listing_id")
            asking_price = result.get("asking_price")
            area_m2 = result.get("area_m2")

            col1.metric("Listing ID", listing_id if listing_id else "Not found")

            if asking_price is not None:
                col2.metric("Asking Price", f"R$ {asking_price:,.0f}")
            else:
                col2.metric("Asking Price", "Not found")

            if area_m2 is not None:
                col3.metric("Area", f"{area_m2} m²")
            else:
                col3.metric("Area", "Not found")

            col4.metric("Bedrooms", result.get("bedrooms"))
            col5.metric("Neighborhood", result.get("neighborhood"))
            
            col6.metric("Condo Fee", f"R$ {result.get('condo_fee'):,.0f}" if result.get("condo_fee") else "Not found")
            
            col7.metric("Benchmark R$/m²", f"R$ {result.get('avg_price_m2'):,.0f}" if result.get("avg_price_m2") else "Not found")
            col8.metric("Market Gap", f"{result.get('market_gap') * 100:.2f}%" if result.get("market_gap") is not None else "Not found")
            col9.metric("Recommendation", result.get("recommendation"))

            st.write("Source:", result.get("source"))
            st.write("URL:", result.get("listing_url"))
            st.write("Page title:", result.get("page_title"))

            with st.expander("Raw extracted data"):
                st.json(result)

        else:
            st.warning("Please paste a property URL.")


# -----------------------------
# DATABASE
# -----------------------------
elif page == "🗄️ Database":

    st.title("🗄️ Property Database")

    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/copetti_capital.db")

    df = pd.read_sql_query(
        """
        SELECT
            listing_id,
            source,
            neighborhood,
            cep,
            asking_price,
            condo_fee,
            area_m2,
            rent_m2 AS price_per_m2,
            bedrooms,
            recommendation,
            status,
            date_collected
        FROM properties
        ORDER BY date_collected DESC
        """,
        conn,
    )

    conn.close()

    st.dataframe(df, use_container_width=True)

# -----------------------------
# MARKET INTELLIGENCE
# -----------------------------
elif page == "📊 Market Intelligence":

    st.title("📊 Market Intelligence")

    benchmarks = get_market_benchmarks()

    if benchmarks.empty:
        st.info("No market benchmarks available yet. Analyze more properties first.")
    else:
        st.subheader("Neighborhood Benchmarks")
        st.dataframe(benchmarks, use_container_width=True)
        
# -----------------------------
# MAP
# -----------------------------
elif page == "🗺️ Map":

    st.title("🗺️ Investment Map")
    st.info("Interactive map coming soon.")


# -----------------------------
# PORTFOLIO
# -----------------------------
elif page == "💼 Portfolio":

    st.title("💼 Portfolio")
    st.info("Portfolio manager coming soon.")