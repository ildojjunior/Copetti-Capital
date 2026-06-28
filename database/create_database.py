import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "copetti_capital.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.close()

    print(f"Database created successfully at: {DB_PATH}")

if __name__ == "__main__":
    create_database()
