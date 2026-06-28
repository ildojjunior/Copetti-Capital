import streamlit as st
from streamlit.components.v1 import html

from database.db_utils import get_properties_dataframe
from maps.property_map import build_property_map


def show_map_page():
    st.title("🗺️ Investment Map")
    st.write("Map of analyzed properties.")

    properties = get_properties_dataframe()

    property_map = build_property_map(properties)

    html(
        property_map._repr_html_(),
        height=600,
    )