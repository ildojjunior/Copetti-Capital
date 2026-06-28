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
        reference[row["location_code"]] = [
            row["latitude"],
            row["longitude"],
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

        coords = location_reference.get(location_code)

        if coords is None:
            continue

        lat, lon = coords

        popup_text = f"""
        <b>Listing:</b> {row.get("listing_id")}<br>
        <b>Location:</b> {location_code}<br>
        <b>Neighborhood:</b> {row.get("neighborhood")}<br>
        <b>Price:</b> R$ {row.get("asking_price")}<br>
        <b>Score:</b> {row.get("investment_score")}<br>
        <b>Recommendation:</b> {row.get("recommendation")}
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(m)

    return m