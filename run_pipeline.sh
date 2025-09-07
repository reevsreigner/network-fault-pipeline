#!/bin/bash

# This script runs the entire data pipeline in the correct sequence.
# Use 'set -e' to exit immediately if any command fails.
set -e

# --- Introduction ---
echo "🚀 Starting the Network KPI Fault Prediction Pipeline..."

# --- Activate Virtual Environment ---
# Check if the virtual environment exists and activate it.
if [ -d ".venv" ]; then
    echo "🐍 Activating Python virtual environment..."
    # Activation command differs for Windows Git Bash vs macOS/Linux
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
else
    echo "❌ Error: Virtual environment '.venv' not found. Please run setup first."
    exit 1
fi

# --- Run Pipeline Stages ---
echo "---"
echo "STEP 1: Running Ingestion Script..."
python src/ingest.py

echo "---"
echo "STEP 2: Running Cleaning & Transformation Script..."
python src/clean_transform.py

echo "---"
echo "STEP 3: Running Database Loading Script..."
python src/load.py

echo "---"
echo "STEP 4: Running Model Training Script..."
python src/train_model.py

# --- Conclusion ---
echo "---"
echo "✅ Pipeline executed successfully!"
echo "📈 To view the results, launch the dashboard with the command:"
echo "streamlit run src/dashboard.py"

