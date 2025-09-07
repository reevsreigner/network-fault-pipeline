import logging
import pandas as pd
import sqlite3
from pathlib import Path

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CURATED_DATA_PATH = BASE_DIR / "data" / "curated" / "kpi_metrics.parquet"
DB_DIR = BASE_DIR / "data" / "db"
DB_PATH = DB_DIR / "telecom_kpi.db"
TABLE_NAME = "kpi_metrics"

# --- Main Loading Function ---
def load_data_to_db():
    """
    Reads the curated Parquet file and loads it into a SQLite database table.
    """
    logging.info("--- Starting Database Loading Phase ---")

    # Read the curated data
    try:
        df = pd.read_parquet(CURATED_DATA_PATH)
        logging.info("Curated Parquet file loaded successfully.")
    except FileNotFoundError:
        logging.error(f"FATAL: Curated data not found at {CURATED_DATA_PATH}")
        raise

    # Load data into SQLite
    try:
        # Ensure the database directory exists
        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # Connect to the SQLite database (it will be created if it doesn't exist)
        conn = sqlite3.connect(DB_PATH)
        logging.info(f"Established connection to SQLite database at '{DB_PATH}'")
        
        # Load the DataFrame into a table
        # 'if_exists='replace'' will drop the table first if it exists,
        # making the script idempotent (rerunnable).
        df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
        
        # Verify the load by counting rows
        row_count = pd.read_sql(f"SELECT COUNT(*) FROM {TABLE_NAME}", conn).iloc[0, 0]
        
        conn.close()
        
        logging.info(f"SUCCESS: Loaded {row_count} rows into table '{TABLE_NAME}'.")

    except Exception as e:
        logging.error(f"FAILURE: Could not load data to SQLite. Reason: {e}")
        raise

    logging.info("--- Database Loading Phase Complete ---")


# --- Script Execution ---
if __name__ == "__main__":
    load_data_to_db()