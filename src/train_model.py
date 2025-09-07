import logging
import pandas as pd
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
CURATED_DATA_PATH = BASE_DIR / "data" / "curated" / "kpi_metrics.parquet"
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "fault_predictor.pkl"

# --- Main Training Function ---
def train_model():
    """Trains, evaluates, and saves the best fault prediction model."""
    logging.info("--- Starting Model Training Phase ---")

    # Load data
    df = pd.read_parquet(CURATED_DATA_PATH)
    logging.info("Curated data loaded successfully.")

    # Prepare data for modeling
    features = ['Latency (ms)', 'Signal Strength (dBm)', 'Data Throughput (Mbps)']
    target = 'fault_flag'

    X = df[features]
    y = df[target]

    # Drop rows with NaN values in the selected features for simplicity
    X = X.dropna()
    y = y[X.index] # Ensure target aligns with features after dropping NaNs
    
    logging.info(f"Prepared data with {len(X)} samples.")

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logging.info("Data split into training and testing sets.")

    # Initialize models with class_weight='balanced' to handle imbalance
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(random_state=42, class_weight='balanced')
    }

    best_model = None
    best_recall = -1.0 # Initialize with a value lower than any possible recall

    # Train and evaluate models
    for name, model in models.items():
        logging.info(f"--- Training {name} ---")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Evaluation
        accuracy = accuracy_score(y_test, y_pred)
        # For logging, use target_names for readability
        report_str = classification_report(y_test, y_pred, target_names=['No Fault (0)', 'Fault (1)'])
        
        logging.info(f"Accuracy: {accuracy:.4f}")
        logging.info("Classification Report:\n" + report_str)
        logging.info("Confusion Matrix:\n" + str(confusion_matrix(y_test, y_pred)))
        
        # For code logic, use the dictionary version with default keys
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        # *** FIX IS HERE: Use the string '1' to access the fault class ***
        recall_fault = report_dict['1']['recall']

        if recall_fault > best_recall:
            best_recall = recall_fault
            best_model = model
            logging.info(f"New best model found: {name} with Recall (Fault) = {recall_fault:.4f}")

    # Save the best model
    if best_model:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(best_model, f)
        logging.info(f"SUCCESS: Best model ({best_model.__class__.__name__}) saved to '{MODEL_PATH}'")
    else:
        logging.warning("No best model was selected.")

    logging.info("--- Model Training Phase Complete ---")

if __name__ == "__main__":
    train_model()