import streamlit as st
from PIL import Image
from pathlib import Path
from database.db_utils import get_dashboard_metrics

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
        "🗺️ Map",
        "💼 Portfolio"
    ]
)

# -----------------------------
# Header
# -----------------------------
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
            st.success("Property received!")
            st.write(property_url)

        else:
            st.warning("Please paste a property URL.")

# -----------------------------
# DATABASE
# -----------------------------
elif page == "🗄️ Database":

    st.title("🗄️ Property Database")
    st.info("Database viewer coming soon.")

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