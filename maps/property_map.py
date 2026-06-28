import folium
import pandas as pd
from pathlib import Path


LOCATION_REFERENCE_FILE = Path("data/location_reference.csv")


def load_location_reference():
    """
    Loads known coordinates for Brasília location codes.
    Examples: CLN213, SGAN911, CRNW510.
    """

    if not LOCATION_REFERENCE_FILE.exists():
        return {}

    df = pd.read_csv(LOCATION_REFERENCE_FILE)

    reference = {}

    for _, row in df.iterrows():
        code = str(row["location_code"]).strip().upper()
        reference[code] = [
            float(row["latitude"]),
            float(row["longitude"]),
        ]

    return reference


def build_property_map(properties_df):
    """
    Builds an interactive map of analyzed properties.
    """

    center_lat = -15.7939
    center_lon = -47.8828

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
    )

    if properties_df.empty:
        return m

    location_reference = load_location_reference()

    for _, row in properties_df.iterrows():
        location_code = row.get("location_code")

        if pd.isna(location_code):
            continue

        location_code = str(location_code).strip().upper()
        coords = location_reference.get(location_code)

        if coords is None:
            continue

        lat, lon = coords

        price = row.get("asking_price")
        area = row.get("area_m2")
        score = row.get("investment_score")
        recommendation = row.get("recommendation")

        price_text = f"R$ {price:,.0f}" if pd.notna(price) else "Not available"
        area_text = f"{area:.1f} m²" if pd.notna(area) else "Not available"
        score_text = f"{score:.0f}/100" if pd.notna(score) else "Not available"
        recommendation_text = (
            str(recommendation).upper()
            if pd.notna(recommendation)
            else "Not available"
        )

        popup_text = f"""
        <b>Listing:</b> {row.get("listing_id")}<br>
        <b>Location:</b> {location_code}<br>
        <b>Neighborhood:</b> {row.get("neighborhood")}<br>
        <b>Price:</b> {price_text}<br>
        <b>Area:</b> {area_text}<br>
        <b>Score:</b> {score_text}<br>
        <b>Recommendation:</b> {recommendation_text}
        """

        recommendation_upper = recommendation_text.upper()

        if recommendation_upper == "BUY":
            color = "green"
        elif recommendation_upper == "PASS":
            color = "red"
        elif recommendation_upper == "REVIEW":
            color = "blue"
        else:
            color = "orange"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=f"{location_code} | {price_text}",
            icon=folium.Icon(
                color=color,
                icon="home",
                prefix="fa",
            ),
        ).add_to(m)

    return m