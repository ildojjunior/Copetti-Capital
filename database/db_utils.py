import sqlite3
import pandas as pd

from config import DATABASE_FILE


def get_properties_dataframe():
    conn = sqlite3.connect(DATABASE_FILE)
    df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df


def get_dashboard_metrics():

    df = get_properties_dataframe()

    total_properties = len(df)

    if total_properties == 0:

        return {
            "total_properties": 0,
            "buy_count": 0,
            "negotiate_count": 0,
            "pass_count": 0,
        }

    recommendation = df["recommendation"].fillna("").str.lower()

    return {

        "total_properties": total_properties,

        "buy_count": (recommendation == "buy").sum(),

        "negotiate_count": (recommendation == "negotiate").sum(),

        "pass_count": (recommendation == "pass").sum()

    }