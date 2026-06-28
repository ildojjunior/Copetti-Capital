from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent

# Folders
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"
REPORTS_DIR = BASE_DIR / "reports"
EXPORTS_DIR = BASE_DIR / "exports"

# Files
DATABASE_FILE = DATA_DIR / "copetti_capital.db"
LOGO_FILE = ASSETS_DIR / "logo.png"