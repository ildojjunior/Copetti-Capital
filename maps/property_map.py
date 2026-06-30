import folium
import pandas as pd

from pathlib import Path
from folium.plugins import MarkerCluster


LOCATION_REFERENCE_FILE = Path("reference_data/brasilia_locations.csv")


def load_location_reference():
    """
    Loads the Brasília location reference database.
    """

    if not LOCATION_REFERENCE_FILE.exists():
        return {}

    df = pd.read_csv(LOCATION_REFERENCE_FILE)

    reference = {}

    for _, row in df.iterrows():
        code = str(row["location_code"]).strip().upper()

        reference[code] = (
            float(row["latitude"]),
            float(row["longitude"]),
        )

    return reference


def build_property_map(properties_df):
    """
    Builds the interactive investment map.
    """

    # Brasília center
    m = folium.Map(
        location=[-15.7939, -47.8828],
        zoom_start=12,
        tiles="CartoDB Positron",
    )

    marker_cluster = MarkerCluster().add_to(m)

    if properties_df.empty:
        return m

    location_reference = load_location_reference()

    for _, row in properties_df.iterrows():

        ####################################
        # Coordinates
        ####################################

        location_code = row.get("location_code")

        if pd.isna(location_code):
            continue

        location_code = str(location_code).strip().upper()

        coords = location_reference.get(location_code)

        if coords is None:
            continue

        lat, lon = coords

        ####################################
        # Property information
        ####################################

        price = row.get("asking_price")
        area = row.get("area_m2")
        score = row.get("investment_score")
        recommendation = row.get("recommendation")
        gross_yield = row.get("gross_yield")
        fair_value = row.get("estimated_fair_value")

        recommendation_text = (
            str(recommendation).strip().upper()
            if pd.notna(recommendation)
            else "UNKNOWN"
        )

        ####################################
        # Marker color
        ####################################

        if recommendation_text == "BUY":
            color = "green"

        elif recommendation_text == "NEGOTIATE":
            color = "orange"

        elif recommendation_text == "REVIEW":
            color = "orange"

        elif recommendation_text == "PASS":
            color = "red"

        else:
            color = "gray"

        ####################################
        # Marker size
        ####################################

        if pd.notna(score):
            radius = max(6, min(18, score / 6))
        else:
            radius = 6

        ####################################
        # Formatting
        ####################################

        price_text = (
            f"R$ {price:,.0f}"
            if pd.notna(price)
            else "Not available"
        )

        fair_value_text = (
            f"R$ {fair_value:,.0f}"
            if pd.notna(fair_value)
            else "Not available"
        )

        area_text = (
            f"{area:.1f} m²"
            if pd.notna(area)
            else "Not available"
        )

        yield_text = (
            f"{gross_yield:.2f}%"
            if pd.notna(gross_yield)
            else "Not available"
        )

        score_text = (
            f"{score:.0f}/100"
            if pd.notna(score)
            else "Not available"
        )

        ####################################
        # Popup
        ####################################

        popup_html = f"""
        <div style="width:260px">

        <h4>{location_code}</h4>

        <b>Listing:</b> {row.get("listing_id")}<br>

        <b>Neighborhood:</b> {row.get("neighborhood")}<br><br>

        <b>Asking Price</b><br>
        {price_text}<br><br>

        <b>Estimated Fair Value</b><br>
        {fair_value_text}<br><br>

        <b>Area</b><br>
        {area_text}<br><br>

        <b>Investment Score</b><br>
        {score_text}<br><br>

        <b>Gross Yield</b><br>
        {yield_text}<br><br>

        <b>Recommendation</b><br>
        {recommendation_text}

        </div>
        """

        ####################################
        # Circle marker
        ####################################

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2,
            tooltip=f"{location_code} • {price_text}",
            popup=folium.Popup(popup_html, max_width=320),
        ).add_to(marker_cluster)

    return m