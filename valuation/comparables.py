import sqlite3
import pandas as pd

from config import DATABASE_FILE


def find_comparable_properties(result: dict, max_results: int = 10):
    """
    Finds comparable properties from the existing database.

    Version 1:
    - Same neighborhood
    - Similar area within +/- 20%
    - Must have price per m²
    """

    neighborhood = result.get("neighborhood")
    area_m2 = result.get("area_m2")

    if not neighborhood or not area_m2:
        return pd.DataFrame()

    min_area = area_m2 * 0.8
    max_area = area_m2 * 1.2

    conn = sqlite3.connect(DATABASE_FILE)

    df = pd.read_sql_query(
        """
        SELECT
            listing_id,
            source,
            neighborhood,
            asking_price,
            area_m2,
            rent_m2 AS price_per_m2,
            bedrooms,
            condo_fee,
            recommendation,
            date_collected
        FROM properties
        WHERE
            neighborhood = ?
            AND area_m2 BETWEEN ? AND ?
            AND rent_m2 IS NOT NULL
            AND rent_m2 > 0
        ORDER BY ABS(area_m2 - ?) ASC
        LIMIT ?
        """,
        conn,
        params=(neighborhood, min_area, max_area, area_m2, max_results),
    )

    conn.close()

    return df

def summarize_comparables(comparables: pd.DataFrame):
    """
    Creates summary statistics from comparable properties.
    """

    if comparables.empty:
        return {
            "comparable_count": 0,
            "comparable_avg_price_m2": None,
            "comparable_median_price_m2": None,
        }

    return {
        "comparable_count": len(comparables),
        "comparable_avg_price_m2": round(comparables["price_per_m2"].mean(), 2),
        "comparable_median_price_m2": round(comparables["price_per_m2"].median(), 2),
    }