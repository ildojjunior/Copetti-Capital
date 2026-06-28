def generate_investment_summary(result: dict):
    recommendation = result.get("recommendation", "Review")
    score = result.get("investment_score", "N/A")
    score_label = result.get("score_label", "Review")
    market_gap = result.get("market_gap")
    neighborhood = result.get("neighborhood", "the selected neighborhood")

    if market_gap is not None:
        market_gap_text = f"{market_gap * 100:.2f}%"
    else:
        market_gap_text = "not available"

    summary = (
        f"**{score_label}** — This property receives an investment score of "
        f"**{score}/100** and a recommendation of **{recommendation}**. "
        f"The property is located in **{neighborhood}** and has a market gap of "
        f"**{market_gap_text}** compared with the current benchmark."
    )

    return summary