def estimate_weighted_fair_value(result: dict, comparables):
    """
    Estimates fair value using comparable properties weighted by similarity score.
    """

    area_m2 = result.get("area_m2")

    if area_m2 is None or comparables.empty:
        result["weighted_avg_price_m2"] = None
        result["weighted_fair_value"] = None
        result["weighted_avm_method"] = "No comparables available"
        return result

    if "similarity_score" not in comparables.columns:
        result["weighted_avg_price_m2"] = None
        result["weighted_fair_value"] = None
        result["weighted_avm_method"] = "No similarity scores available"
        return result

    total_weight = comparables["similarity_score"].sum()

    if total_weight == 0:
        result["weighted_avg_price_m2"] = None
        result["weighted_fair_value"] = None
        result["weighted_avm_method"] = "Similarity weights are zero"
        return result

    weighted_avg_price_m2 = (
        comparables["price_per_m2"] * comparables["similarity_score"]
    ).sum() / total_weight

    weighted_fair_value = weighted_avg_price_m2 * area_m2

    result["weighted_avg_price_m2"] = round(weighted_avg_price_m2, 2)
    result["weighted_fair_value"] = round(weighted_fair_value, 2)
    result["weighted_avm_method"] = "Comparable-weighted valuation"

    return result