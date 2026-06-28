import streamlit as st
from PIL import Image
from pathlib import Path

from valuation.valuation_engine import evaluate_property
from database.db_utils import get_dashboard_metrics, save_analyzed_property
from scraper.dfimoveis import parse_dfimoveis_listing
from valuation.market_intelligence import get_market_benchmarks
from scoring.investment_score import calculate_investment_score

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
                result = calculate_investment_score(result)

            st.success("Property analyzed successfully!")

            save_analyzed_property(result)
            st.info("Property saved to database.")

            st.subheader("Extracted Property Data")
            
            left_col, right_col = st.columns(2)
            
            with left_col:
                st.subheader("Property Data")
                st.metric("Listing ID", result.get("listing_id"))
                st.metric("Asking Price", f"R$ {result.get('asking_price'):,.0f}" if result.get("asking_price") else "Not found")
                st.metric("Area", f"{result.get('area_m2')} m²" if result.get("area_m2") else "Not found")
                st.metric("Bedrooms", result.get("bedrooms"))
                st.metric("Condo Fee", f"R$ {result.get('condo_fee'):,.0f}" if result.get("condo_fee") else "Not found")
                st.metric("Neighborhood", result.get("neighborhood"))
            
            with right_col:
                 st.subheader("Investment Analysis")
                 
                 st.metric("Investment Score", f"{result.get('investment_score')}/100")
                 st.markdown(f"**{result.get('score_label')}**")
                 
                 st.metric("Recommendation", result.get("recommendation"))
                 st.metric("Price per m²", f"R$ {result.get('price_per_m2'):,.0f}" if result.get("price_per_m2") else "Not found")
                 st.metric("Benchmark R$/m²", f"R$ {result.get('avg_price_m2'):,.0f}" if result.get("avg_price_m2") else "Not found")
                 st.metric("Market Gap", f"{result.get('market_gap') * 100:.2f}%" if result.get("market_gap") is not None else "Not found")
                 st.markdown("### Why?")
                 
                 for reason in result.get("score_reasons", []):
                 st.write(f"✓ {reason}")

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