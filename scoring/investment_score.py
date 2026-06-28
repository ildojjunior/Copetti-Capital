def get_score_label(score):
    """
    Returns a human-readable label based on the investment score.
    """

    if score is None:
        return "Review"

    if score >= 80:
        return "Excellent Opportunity"

    if score >= 65:
        return "Good Opportunity"

    if score >= 50:
        return "Worth Negotiating"

    if score >= 35:
        return "Weak Opportunity"

    return "Avoid"


def calculate_investment_score(result: dict):
    """
    Calculates an investment score between 0 and 100 based on
    the information currently available.
    """

    score = 50
    reasons = []

    market_gap = result.get("market_gap")

    if market_gap is not None:

        if market_gap <= -0.10:
            score += 30
            reasons.append("Property is significantly below market price.")

        elif market_gap <= 0:
            score += 15
            reasons.append("Property is slightly below market price.")

        elif market_gap <= 0.05:
            score += 5
            reasons.append("Property is close to market value.")

        else:
            score -= 20
            reasons.append("Property appears overpriced.")

    # Keep the score between 0 and 100
    score = max(0, min(score, 100))

    result["investment_score"] = score
    result["score_label"] = get_score_label(score)
    result["score_reasons"] = reasons

    return result