import streamlit as st
from streamlit_folium import st_folium

from database.db_utils import get_properties_dataframe
from maps.property_map import build_property_map


def show_map_page():
    st.title("🗺️ Investment Map")
    st.write("Map of analyzed properties.")

    properties = get_properties_dataframe()
    property_map = build_property_map(properties)

    st_folium(
        property_map,
        width=1400,
        height=750,
    )