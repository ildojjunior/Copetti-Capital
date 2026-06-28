import streamlit as st
from database.db_utils import get_dashboard_metrics


def show_dashboard():

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