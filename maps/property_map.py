import folium


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

    return m