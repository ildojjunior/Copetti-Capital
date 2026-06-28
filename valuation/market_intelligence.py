import sqlite3
import pandas as pd

from config import DATABASE_FILE


def get_market_benchmarks():
    conn = sqlite3.connect(DATABASE_FILE)

    df = pd.read_sql_query(
        """
        SELECT
            neighborhood,
            area_m2,
            asking_price,
            rent_m2 AS price_per_m2
        FROM properties
        WHERE
            neighborhood IS NOT NULL
            AND rent_m2 IS NOT NULL
            AND rent_m2 > 0
        """,
        conn,
    )

    conn.close()

    if df.empty:
        return df

    benchmarks = (
        df.groupby("neighborhood")
        .agg(
            observations=("price_per_m2", "count"),
            avg_price_m2=("price_per_m2", "mean"),
            median_price_m2=("price_per_m2", "median"),
            min_price_m2=("price_per_m2", "min"),
            max_price_m2=("price_per_m2", "max"),
        )
        .reset_index()
    )

    return benchmarks