def calculate_investment_score(result: dict):

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

    score = max(0, min(score, 100))

    result["investment_score"] = score
    result["score_reasons"] = reasons

    return result