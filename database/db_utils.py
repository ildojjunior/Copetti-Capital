import sqlite3
import pandas as pd
import uuid 

from datetime import datetime
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

def save_analyzed_property(result: dict):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        """
        INSERT INTO properties (
    property_id,
    source,
    listing_id,
    listing_url,
    date_collected,
    last_updated,
    neighborhood,
    cep,
    asking_price,
    area_m2,
    bedrooms,
    status,
    recommendation
    )
       
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
    str(uuid.uuid4()),
    result.get("source"),
    result.get("listing_id"),
    result.get("listing_url"),
    now,
    now,
    result.get("neighborhood"),
    result.get("cep_partial"),
    result.get("asking_price"),
    result.get("area_m2"),
    result.get("bedrooms"),
    "analyzed",
    "negotiate",
),
    )

    conn.commit()
    conn.close()