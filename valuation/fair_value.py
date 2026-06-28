def estimate_fair_value(result: dict):
    """
    Estimates a simple fair value based on neighborhood benchmark price per m².
    """

    area_m2 = result.get("area_m2")
    avg_price_m2 = result.get("avg_price_m2")
    asking_price = result.get("asking_price")

    if not area_m2 or not avg_price_m2:
        result["estimated_fair_value"] = None
        result["discount_to_fair_value"] = None
        result["suggested_offer_price"] = None
        return result

    estimated_fair_value = area_m2 * avg_price_m2

    if asking_price:
        discount_to_fair_value = (estimated_fair_value - asking_price) / estimated_fair_value
    else:
        discount_to_fair_value = None

    suggested_offer_price = estimated_fair_value * 0.90

    result["estimated_fair_value"] = round(estimated_fair_value, 2)
    result["discount_to_fair_value"] = round(discount_to_fair_value, 4) if discount_to_fair_value is not None else None
    result["suggested_offer_price"] = round(suggested_offer_price, 2)

    return result