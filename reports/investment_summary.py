def generate_investment_summary(result: dict):
    """
    Generates an executive investment summary for the analyzed property.
    """

    recommendation = result.get("recommendation", "Review")
    score = result.get("investment_score", "N/A")
    score_label = result.get("score_label", "Review")

    asking_price = result.get("asking_price")
    price_per_m2 = result.get("price_per_m2")
    benchmark = result.get("avg_price_m2")
    market_gap = result.get("market_gap")
    neighborhood = result.get("neighborhood", "Unknown")

    lines = []

    # --------------------------------------------------
    # Executive conclusion
    # --------------------------------------------------

    lines.append(
        f"### {score_label} ({score}/100)"
    )

    lines.append(
        f"**Recommendation:** {recommendation}"
    )

    lines.append("")

    # --------------------------------------------------
    # Property overview
    # --------------------------------------------------

    lines.append("#### Property Overview")

    if asking_price:
        lines.append(f"- Asking price: **R$ {asking_price:,.0f}**")

    if price_per_m2:
        lines.append(f"- Price per m²: **R$ {price_per_m2:,.0f}**")

    if benchmark:
        lines.append(f"- Neighborhood benchmark: **R$ {benchmark:,.0f}/m²**")

    if market_gap is not None:
        lines.append(
            f"- Market gap: **{market_gap*100:.2f}%**"
        )

    lines.append("")

    # --------------------------------------------------
    # Interpretation
    # --------------------------------------------------

    lines.append("#### Interpretation")

    if market_gap is None:
        lines.append(
            "- There is not enough market information to evaluate this property."
        )

    elif market_gap <= -0.10:
        lines.append(
            "- The asking price is substantially below the neighborhood benchmark."
        )
        lines.append(
            "- This may represent an attractive buying opportunity."
        )

    elif market_gap <= 0:
        lines.append(
            "- The property is slightly below the neighborhood benchmark."
        )
        lines.append(
            "- There appears to be room for negotiation."
        )

    elif market_gap <= 0.05:
        lines.append(
            "- The asking price is close to market value."
        )
        lines.append(
            "- Financial returns will depend on rental income and financing conditions."
        )

    else:
        lines.append(
            "- The asking price is above the neighborhood benchmark."
        )
        lines.append(
            "- Negotiation is recommended before considering acquisition."
        )

    lines.append("")

    # --------------------------------------------------
    # Next analyses
    # --------------------------------------------------

    lines.append("#### Next Steps")

    lines.append("- Estimate rental income.")
    lines.append("- Simulate financing.")
    lines.append("- Estimate cash flow.")
    lines.append("- Calculate gross and net rental yield.")
    lines.append("- Estimate long-term appreciation potential.")

    return "\n".join(lines)