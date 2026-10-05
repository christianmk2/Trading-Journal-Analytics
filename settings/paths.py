from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
CHARTS_DIR = PROJECT_ROOT / "charts"
DASHBOARD_DIR = PROJECT_ROOT / "v1-dashboard_excel"
SQL_DIR = PROJECT_ROOT / "sql"
SQLITE_SQL_DIR = SQL_DIR / "sqlite"
POSTGRES_SQL_DIR = SQL_DIR / "postgres"
SQLITE_DB_PATH = DATA_DIR / "trading_journal.db"
ENV_FILE = PROJECT_ROOT / ".env"