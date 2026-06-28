import pandas as pd
from pathlib import Path


REFERENCE_FILE = Path("data/neighborhood_reference.csv")


def load_neighborhood_reference():
    return pd.read_csv(REFERENCE_FILE)


def calculate_market_gap(price_per_m2, avg_price_m2):
    if price_per_m2 is None or avg_price_m2 is None or avg_price_m2 == 0:
        return None

    return round((price_per_m2 - avg_price_m2) / avg_price_m2, 4)


def classify_recommendation(market_gap):
    if market_gap is None:
        return "Review"

    if market_gap <= -0.10:
        return "BUY"

    if market_gap <= 0.05:
        return "NEGOTIATE"

    return "PASS"


def evaluate_property(result: dict):
    reference = load_neighborhood_reference()

    neighborhood = result.get("neighborhood")
    property_type = result.get("property_type")

    match = reference[
        (reference["neighborhood"] == neighborhood)
        & (reference["property_type"] == property_type)
    ]

    if match.empty:
        result["avg_price_m2"] = None
        result["market_gap"] = None
        result["recommendation"] = "Review"
        return result

    avg_price_m2 = float(match.iloc[0]["avg_price_m2"])
    price_per_m2 = result.get("price_per_m2")

    market_gap = calculate_market_gap(price_per_m2, avg_price_m2)

    result["avg_price_m2"] = avg_price_m2
    result["market_gap"] = market_gap
    result["recommendation"] = classify_recommendation(market_gap)

    return result