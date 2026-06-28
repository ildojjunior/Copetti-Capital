import sqlite3

import pandas as pd

from config import DATABASE_FILE


def calculate_similarity_score(target: dict, comparable: dict):
    """
    Calculates a similarity score (0-100) between the target property
    and a comparable property.

    Version 1 considers:
    - Area
    - Bedrooms

    The SQL query already guarantees the same neighborhood.
    """

    score = 100

    # -------------------------
    # Area
    # -------------------------
    target_area = target.get("area_m2")
    comparable_area = comparable.get("area_m2")

    if target_area and comparable_area:
        area_difference = abs(target_area - comparable_area) / target_area
        score -= area_difference * 100

    # -------------------------
    # Bedrooms
    # -------------------------
    target_bedrooms = target.get("bedrooms")
    comparable_bedrooms = comparable.get("bedrooms")

    if (
        target_bedrooms is not None
        and comparable_bedrooms is not None
        and target_bedrooms != comparable_bedrooms
    ):
        score -= 15

    score = max(0, min(score, 100))

    return round(score, 1)


def explain_similarity(target: dict, comparable: dict):
    """
    Generates a human-readable explanation for why two
    properties are considered comparable.
    """

    reasons = []

    # Neighborhood
    if target.get("neighborhood") == comparable.get("neighborhood"):
        reasons.append("Same neighborhood")

    # Area
    target_area = target.get("area_m2")
    comparable_area = comparable.get("area_m2")

    if target_area and comparable_area:
        diff = abs(target_area - comparable_area) / target_area * 100
        reasons.append(f"Area difference: {diff:.1f}%")

    # Bedrooms
    if target.get("bedrooms") == comparable.get("bedrooms"):
        reasons.append("Same bedrooms")

    return " • ".join(reasons)


def find_comparable_properties(result: dict, max_results: int = 10):
    """
    Finds comparable properties stored in the database.

    Current filters:
    - Same neighborhood
    - Area within ±20%
    - Price/m² available
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

    if df.empty:
        return df

    # Remove duplicate listings
    df = df.drop_duplicates(subset="listing_id", keep="last")

    # Calculate similarity
    df["similarity_score"] = df.apply(
        lambda row: calculate_similarity_score(result, row.to_dict()),
        axis=1,
    )

    # Explain similarity
    df["similarity_reason"] = df.apply(
        lambda row: explain_similarity(result, row.to_dict()),
        axis=1,
    )

    # Most similar first
    df = df.sort_values("similarity_score", ascending=False)

    return df


def summarize_comparables(comparables: pd.DataFrame):
    """
    Creates summary statistics for comparable properties.
    """

    if comparables.empty:
        return {
            "comparable_count": 0,
            "comparable_avg_price_m2": None,
            "comparable_median_price_m2": None,
        }

    return {
        "comparable_count": int(len(comparables)),
        "comparable_avg_price_m2": float(
            round(comparables["price_per_m2"].mean(), 2)
        ),
        "comparable_median_price_m2": float(
            round(comparables["price_per_m2"].median(), 2)
        ),
    }

def calculate_valuation_confidence(comparables: pd.DataFrame):
    """
    Calculates a confidence level for the valuation.
    """

    if comparables.empty:
        return {
            "confidence_score": 0.0,
            "confidence_label": "Low confidence",
        }

    comparable_count = len(comparables)
    avg_similarity = float(comparables["similarity_score"].mean())

    score = min(
        100,
        (comparable_count * 10) + (avg_similarity * 0.5),
    )

    if score >= 80:
        label = "High confidence"
    elif score >= 50:
        label = "Medium confidence"
    else:
        label = "Low confidence"

    return {
        "confidence_score": round(float(score), 1),
        "confidence_label": label,
    }