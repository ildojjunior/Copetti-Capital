import sqlite3
import uuid
from datetime import datetime

import pandas as pd

from config import DATABASE_FILE


# ==========================================================
# READ FUNCTIONS
# ==========================================================

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
        "pass_count": (recommendation == "pass").sum(),
    }


# ==========================================================
# PROPERTY EXISTENCE
# ==========================================================

def property_exists(listing_id, source):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM properties
        WHERE listing_id = ?
        AND source = ?
        """,
        (listing_id, source),
    )

    exists = cursor.fetchone()[0] > 0

    conn.close()

    return exists


# ==========================================================
# PRICE CHANGE DETECTION
# ==========================================================

def price_changed(result):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            asking_price,
            condo_fee,
            iptu
        FROM properties
        WHERE listing_id = ?
        AND source = ?
        """,
        (
            result.get("listing_id"),
            result.get("source"),
        ),
    )

    row = cursor.fetchone()

    conn.close()

    # New listing
    if row is None:
        return True

    return (
        row[0] != result.get("asking_price")
        or row[1] != result.get("condo_fee")
        or row[2] != result.get("iptu")
    )


# ==========================================================
# PRICE HISTORY
# ==========================================================

def save_price_history(result):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        """
        INSERT INTO property_price_history(
            history_id,
            listing_id,
            source,
            date_recorded,
            asking_price,
            condo_fee,
            iptu
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(uuid.uuid4()),
            result.get("listing_id"),
            result.get("source"),
            now,
            result.get("asking_price"),
            result.get("condo_fee"),
            result.get("iptu"),
        ),
    )

    conn.commit()
    conn.close()

    print(
        f"Saved price history for {result.get('listing_id')}"
    )


# ==========================================================
# UPDATE PROPERTY
# ==========================================================

def update_property(result):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        """
        UPDATE properties
        SET
            last_updated = ?,
            neighborhood = ?,
            location_code = ?,
            asking_price = ?,
            condo_fee = ?,
            iptu = ?,
            area_m2 = ?,
            rent_m2 = ?,
            bedrooms = ?,
            floor = ?,
            estimated_fair_value = ?,
            expected_rent = ?,
            gross_yield = ?,
            net_yield = ?,
            investment_score = ?,
            recommendation = ?
        WHERE listing_id = ?
        AND source = ?
        """,
        (
            now,
            result.get("neighborhood"),
            result.get("location_code"),
            result.get("asking_price"),
            result.get("condo_fee"),
            result.get("iptu"),
            result.get("area_m2"),
            result.get("price_per_m2"),
            result.get("bedrooms"),
            result.get("floor"),
            result.get("estimated_fair_value"),
            result.get("estimated_rent"),
            result.get("gross_yield"),
            result.get("net_yield"),
            result.get("investment_score"),
            result.get("recommendation"),
            result.get("listing_id"),
            result.get("source"),
        ),
    )

    conn.commit()
    conn.close()

    print(
        f"Updated listing {result.get('listing_id')}"
    )

    return True


# ==========================================================
# INSERT PROPERTY
# ==========================================================

def save_analyzed_property(result):

    # Save history only when price-related fields changed
    if price_changed(result):
        save_price_history(result)

    # Update existing property
    if property_exists(
        result.get("listing_id"),
        result.get("source"),
    ):
        update_property(result)
        return False

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
            location_code,
            cep,
            asking_price,
            condo_fee,
            iptu,
            area_m2,
            rent_m2,
            bedrooms,
            floor,
            estimated_fair_value,
            expected_rent,
            gross_yield,
            net_yield,
            investment_score,
            status,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(uuid.uuid4()),
            result.get("source"),
            result.get("listing_id"),
            result.get("listing_url"),
            now,
            now,
            result.get("neighborhood"),
            result.get("location_code"),
            result.get("cep_partial"),
            result.get("asking_price"),
            result.get("condo_fee"),
            result.get("iptu"),
            result.get("area_m2"),
            result.get("price_per_m2"),
            result.get("bedrooms"),
            result.get("floor"),
            result.get("estimated_fair_value"),
            result.get("estimated_rent"),
            result.get("gross_yield"),
            result.get("net_yield"),
            result.get("investment_score"),
            "analyzed",
            result.get("recommendation"),
        ),
    )

    conn.commit()
    conn.close()

    print(
        f"Inserted listing {result.get('listing_id')}"
    )

    return True