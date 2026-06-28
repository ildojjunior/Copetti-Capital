def calculate_investment_metrics(result: dict):
    """
    Basic investment metrics.
    Version 1.0
    """

    asking_price = result.get("asking_price")
    condo_fee = result.get("condo_fee")

    # --------------------------------------------------
    # Temporary rent estimation
    # --------------------------------------------------

    estimated_rent = None

    if asking_price:
        estimated_rent = asking_price * 0.0075

    # --------------------------------------------------
    # Gross Yield
    # --------------------------------------------------

    gross_yield = None

    if asking_price and estimated_rent:
        gross_yield = (estimated_rent * 12) / asking_price

    # --------------------------------------------------
    # Net Yield
    # --------------------------------------------------

    net_yield = None

    if asking_price and estimated_rent:

        annual_costs = (condo_fee or 0) * 12

        net_yield = (
            (estimated_rent * 12 - annual_costs)
            / asking_price
        )

    result["estimated_rent"] = round(estimated_rent, 2) if estimated_rent else None
    result["gross_yield"] = round(gross_yield * 100, 2) if gross_yield else None
    result["net_yield"] = round(net_yield * 100, 2) if net_yield else None

    return result