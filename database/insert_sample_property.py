import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "copetti_capital.db"

sample_property = {
    "property_id": "PROP-000001",
    "listing_id": "1358762",
    "source": "DFImóveis",
    "listing_url": "https://www.dfimoveis.com.br/imovel/kitnet-1-quarto-venda-asa-norte-brasilia-df-cln-213-1358762",
    "date_collected": "2026-06-28",
    "last_updated": "2026-06-28",
    "status": "Active",
    "neighborhood": "Asa Norte",
    "superquadra": "CLN 213",
    "area_m2": 31,
    "bedrooms": 1,
    "bathrooms": 1,
    "asking_price": 285000,
    "expected_rent": 2100,
    "down_payment": 100000,
    "loan_amount": 185000,
    "gross_yield": 0.0884,
    "mortgage_coverage": 1.05,
    "investment_score": 84,
    "recommendation": "Negotiate",
}

columns = ", ".join(sample_property.keys())
placeholders = ", ".join(["?"] * len(sample_property))
values = list(sample_property.values())

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    f"INSERT OR REPLACE INTO properties ({columns}) VALUES ({placeholders})",
    values,
)

conn.commit()
conn.close()

print("Sample property inserted successfully.")
