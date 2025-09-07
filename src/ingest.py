import logging
from pathlib import Path

# --- Configuration ---
# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define project paths using pathlib for OS compatibility
# BASE_DIR is the project root (e.g., 'Network_KPI_Fault_Prediction/')
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
SOURCE_CSV_PATH = RAW_DATA_DIR / "signal_metrics.csv"

# --- Main Ingestion Function ---
def ingest_data():
    """
    Checks if the source data CSV exists and logs the result.
    In a real pipeline, this could also handle copying data from a
    source like an S3 bucket to the local raw directory.
    """
    logging.info("--- Starting Ingestion Phase ---")

    # Check if the source CSV file exists
    if SOURCE_CSV_PATH.exists():
        logging.info(f"SUCCESS: Source data found at '{SOURCE_CSV_PATH}'")
        # For now, we just confirm it exists. The next script will read it.
    else:
        logging.error(f"FAILURE: Source data not found at '{SOURCE_CSV_PATH}'")
        # Raise an error to stop the pipeline if the file is missing
        raise FileNotFoundError(f"Source file not found: {SOURCE_CSV_PATH}")

    logging.info("--- Ingestion Phase Complete ---")

# --- Script Execution ---
if __name__ == "__main__":
    """
    This block allows the script to be run directly from the command line.
    """
    ingest_data()