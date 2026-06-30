import streamlit as st
from PIL import Image
from pathlib import Path

from valuation.valuation_engine import evaluate_property
from database.db_utils import get_dashboard_metrics, save_analyzed_property
from scraper.dfimoveis import parse_dfimoveis_listing
from valuation.market_intelligence import get_market_benchmarks
from scoring.investment_score import calculate_investment_score
from reports.investment_summary import generate_investment_summary
from valuation.fair_value import estimate_fair_value
from finance.investment_metrics import calculate_investment_metrics
from pages.dashboard import show_dashboard
from pages.analyzer import show_analyzer
from pages.map_page import show_map_page
from pages.database_page import show_database_page

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
    show_dashboard()

# -----------------------------
# PROPERTY ANALYZER
# -----------------------------

elif page == "🔍 Property Analyzer":
    show_analyzer()

# -----------------------------
# DATABASE
# -----------------------------
elif page == "🗄️ Database":
    show_database_page()
    
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
    show_map_page()

# -----------------------------
# PORTFOLIO
# -----------------------------
elif page == "💼 Portfolio":

    st.title("💼 Portfolio")
    st.info("Portfolio manager coming soon.")