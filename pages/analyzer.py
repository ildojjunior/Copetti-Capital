import streamlit as st

from database.db_utils import save_analyzed_property
from scraper.dfimoveis import parse_dfimoveis_listing
from valuation.valuation_engine import evaluate_property
from valuation.fair_value import estimate_fair_value
from finance.investment_metrics import calculate_investment_metrics
from scoring.investment_score import calculate_investment_score
from reports.investment_summary import generate_investment_summary
from valuation.comparables import (
    find_comparable_properties,
    summarize_comparables,
)


def show_analyzer():

    st.title("🔍 Property Analyzer")
    st.write("Paste a DFImóveis or Wimoveis property URL.")

    property_url = st.text_input("Property URL")

    if st.button("Analyze Property"):

        if property_url:

            with st.spinner("Analyzing property..."):
                result = parse_dfimoveis_listing(property_url)
                result = evaluate_property(result)
                result = estimate_fair_value(result)
                result = calculate_investment_metrics(result)
                result = calculate_investment_score(result)

                comparables = find_comparable_properties(result)
                comparable_summary = summarize_comparables(comparables)

                summary = generate_investment_summary(result)

            st.success("Property analyzed successfully!")

            save_analyzed_property(result)
            st.info("Property saved to database.")

            st.subheader("Investment Report")

            kpi1, kpi2, kpi3 = st.columns(3)

            with kpi1:
                st.metric(
                    "Investment Score",
                    f"{result.get('investment_score')}/100",
                    result.get("score_label"),
                )

            with kpi2:
                st.metric(
                    "Estimated Fair Value",
                    (
                        f"R$ {result.get('estimated_fair_value'):,.0f}"
                        if result.get("estimated_fair_value")
                        else "Not available"
                    ),
                )

            with kpi3:
                st.metric(
                    "Suggested Offer",
                    (
                        f"R$ {result.get('suggested_offer_price'):,.0f}"
                        if result.get("suggested_offer_price")
                        else "Not available"
                    ),
                )

            st.divider()

            st.markdown("### Executive Summary")
            st.markdown(summary)
            st.divider()

            left_col, right_col = st.columns(2)

            with left_col:
                st.subheader("Property Data")

                st.metric("Listing ID", result.get("listing_id"))

                st.metric(
                    "Asking Price",
                    (
                        f"R$ {result.get('asking_price'):,.0f}"
                        if result.get("asking_price")
                        else "Not found"
                    ),
                )

                st.metric(
                    "Area",
                    (
                        f"{result.get('area_m2')} m²"
                        if result.get("area_m2")
                        else "Not found"
                    ),
                )

                st.metric("Bedrooms", result.get("bedrooms"))

                st.metric(
                    "Condo Fee",
                    (
                        f"R$ {result.get('condo_fee'):,.0f}"
                        if result.get("condo_fee")
                        else "Not found"
                    ),
                )

                st.metric("Neighborhood", result.get("neighborhood"))

                st.write("Source:", result.get("source"))
                st.write("URL:", result.get("listing_url"))

            with right_col:
                st.subheader("Investment Analysis")

                st.metric(
                    "Recommendation",
                    result.get("recommendation"),
                )

                st.metric(
                    "Market Gap",
                    (
                        f"{result.get('market_gap') * 100:.2f}%"
                        if result.get("market_gap") is not None
                        else "Not available"
                    ),
                )

                st.metric(
                    "Price per m²",
                    (
                        f"R$ {result.get('price_per_m2'):,.0f}"
                        if result.get("price_per_m2")
                        else "Not available"
                    ),
                )

                st.metric(
                    "Neighborhood Benchmark",
                    (
                        f"R$ {result.get('avg_price_m2'):,.0f}"
                        if result.get("avg_price_m2")
                        else "Not available"
                    ),
                )

                st.divider()

                st.subheader("Rental Analysis")

                st.metric(
                    "Estimated Rent",
                    (
                        f"R$ {result.get('estimated_rent'):,.0f}"
                        if result.get("estimated_rent")
                        else "Not available"
                    ),
                )

                st.metric(
                    "Gross Yield",
                    (
                        f"{result.get('gross_yield'):.2f}%"
                        if result.get("gross_yield")
                        else "Not available"
                    ),
                )

                st.metric(
                    "Net Yield",
                    (
                        f"{result.get('net_yield'):.2f}%"
                        if result.get("net_yield")
                        else "Not available"
                    ),
                )

                st.divider()

                st.subheader("Why?")

                for reason in result.get("score_reasons", []):
                    st.write(f"✓ {reason}")

            st.divider()
            st.subheader("Comparable Properties")

            if comparable_summary["comparable_count"] == 0:
                st.info("No comparable properties found yet.")

            else:
                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Comparables Found",
                    comparable_summary["comparable_count"],
                )

                c2.metric(
                    "Average Price/m²",
                    f"R$ {comparable_summary['comparable_avg_price_m2']:,.0f}",
                )

                c3.metric(
                    "Median Price/m²",
                    f"R$ {comparable_summary['comparable_median_price_m2']:,.0f}",
                )

                st.dataframe(comparables, use_container_width=True)

            with st.expander("Raw extracted data"):
                st.json(result)

        else:
            st.warning("Please paste a property URL.")
