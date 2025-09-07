import logging
import numpy as np
import pandas as pd
from pathlib import Path

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "signal_metrics.csv"
CURATED_DATA_DIR = BASE_DIR / "data" / "curated"
OUTPUT_PARQUET_PATH = CURATED_DATA_DIR / "kpi_metrics.parquet"

# --- Helper Function for Fault Labeling ---
def label_fault(row):
    """Applies business rules to label a row as a fault (1) or not (0)."""
    if (row["Latency (ms)"] > 200 and row["Data Throughput (Mbps)"] < 1) \
       or (row["Signal Strength (dBm)"] < -100):
        return 1
    else:
        return 0

# --- Main Transformation Function ---
def transform_data():
    """
    Reads raw data, cleans it, engineers features, and saves it
    to a Parquet file in the curated layer.
    """
    logging.info("--- Starting Transformation Phase ---")

    # Read the raw data
    try:
        df = pd.read_csv(RAW_DATA_PATH, parse_dates=['Timestamp'])
        logging.info("Raw data loaded successfully.")
    except FileNotFoundError:
        logging.error(f"FATAL: Raw data not found at {RAW_DATA_PATH}")
        raise

    # 1. Clean Data: Replace 0.0 with NaN where it indicates missing data
    cols_to_clean = [
        'Signal Quality (%)',
        'BB60C Measurement (dBm)',
        'srsRAN Measurement (dBm)',
        'BladeRFxA9 Measurement (dBm)'
    ]
    df[cols_to_clean] = df[cols_to_clean].replace(0.0, np.nan)
    logging.info("Replaced 0.0 with NaN in specified measurement columns.")

    # 2. Normalize Data: Standardize 'Network Type'
    df['Network Type'] = df['Network Type'].replace('LTE', '4G')
    logging.info("Normalized 'LTE' to '4G' in 'Network Type'.")

    # 3. Feature Engineering: Create the 'fault_flag' and other features
    df['fault_flag'] = df.apply(label_fault, axis=1)
    logging.info("Applied fault labeling rules to create 'fault_flag'.")
    
    # Avoid division by zero for the derived feature
    df['Throughput_per_Latency'] = df['Data Throughput (Mbps)'] / df['Latency (ms)'].replace(0, np.nan)
    logging.info("Created 'Throughput_per_Latency' derived feature.")

    # 4. Save Curated Data: Store as Parquet
    try:
        # Ensure the curated directory exists
        CURATED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_parquet(OUTPUT_PARQUET_PATH, index=False)
        logging.info(f"SUCCESS: Transformed data saved to '{OUTPUT_PARQUET_PATH}'")
    except Exception as e:
        logging.error(f"FAILURE: Could not save Parquet file. Reason: {e}")
        raise

    logging.info("--- Transformation Phase Complete ---")


# --- Script Execution ---
if __name__ == "__main__":
    transform_data()