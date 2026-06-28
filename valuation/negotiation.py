"""
Negotiation Strategy Engine

Generates recommended offer prices based on
the estimated fair value and current asking price.
"""


def generate_negotiation_strategy(result: dict):
    """
    Generates three negotiation strategies.

    Returns
    -------
    dict
    """

    asking_price = result.get("asking_price")
    fair_value = result.get("estimated_fair_value")

    if asking_price is None or fair_value is None:
        return None

    aggressive = fair_value * 0.95
    fair = fair_value
    competitive = min(asking_price, fair_value * 1.03)

    discount = (asking_price - fair_value) / asking_price * 100

    return {
        "asking_price": asking_price,
        "fair_value": fair_value,
        "discount_from_asking": round(discount, 1),
        "aggressive_offer": round(aggressive, 0),
        "fair_offer": round(fair, 0),
        "competitive_offer": round(competitive, 0),
    }