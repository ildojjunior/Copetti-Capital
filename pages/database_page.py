import streamlit as st

from database.db_utils import get_properties_dataframe


def show_database_page():
    st.title("🗄️ Database Explorer")
    st.write("Explore scraped and analyzed properties.")

    df = get_properties_dataframe()

    if df.empty:
        st.info("No properties in the database yet.")
        return

    # -----------------------------
    # Filters
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        neighborhood = st.selectbox(
            "Neighborhood",
            ["All"] + sorted(df["neighborhood"].dropna().unique().tolist()),
        )

    with col2:
        recommendation = st.selectbox(
            "Recommendation",
            ["All"] + sorted(df["recommendation"].dropna().unique().tolist()),
        )

    with col3:
        minimum_score = st.slider(
            "Minimum Investment Score",
            0,
            100,
            0,
        )

    filtered = df.copy()

    if neighborhood != "All":
        filtered = filtered[filtered["neighborhood"] == neighborhood]

    if recommendation != "All":
        filtered = filtered[filtered["recommendation"] == recommendation]

    filtered = filtered[
        filtered["investment_score"].fillna(0) >= minimum_score
    ]

    # -----------------------------
    # Metrics
    # -----------------------------
    st.metric("Properties Shown", len(filtered))

    # -----------------------------
    # Table
    # -----------------------------
    columns_to_show = [
        "listing_id",
        "location_code",
        "neighborhood",
        "asking_price",
        "area_m2",
        "rent_m2",
        "gross_yield",
        "net_yield",
        "investment_score",
        "recommendation",
        "last_updated",
    ]

    available_columns = [
        col for col in columns_to_show if col in filtered.columns
    ]

    st.dataframe(
        filtered[available_columns].sort_values(
            by="investment_score",
            ascending=False,
            na_position="last",
        ),
        use_container_width=True,
    )