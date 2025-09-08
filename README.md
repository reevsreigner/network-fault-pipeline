# End-to-End Network Fault Prediction Pipeline

🚀 **Live Demo**
You can view and interact with the live dashboard here:
[https://network-fault-pipeline-3vvqve5jqkpclaumhueyqh.streamlit.app/](https://network-fault-pipeline-3vvqve5jqkpclaumhueyqh.streamlit.app/)

**An end-to-end data pipeline to ingest, clean, and analyze telecommunications data, and train a model to predict network faults.**
The project culminates in a live, interactive Streamlit dashboard.

---

## 1. Project Overview

### 1.1 Objective

To design and implement a scalable data pipeline that ingests raw network KPI data, cleans and transforms it, stores it in a structured database, and uses it to train a machine learning model for fault prediction.
The final output is an interactive dashboard for KPI monitoring and live fault prediction.

### 1.2 Business Value

This project demonstrates a proactive approach to network maintenance. By predicting potential faults based on real-time KPI data, telecom operators can:

* **Reduce Downtime**: Address issues before they cause service outages.
* **Improve Quality of Service (QoS)**: Ensure network availability and reliability.
* **Optimize Maintenance**: Transition from a reactive to a proactive maintenance schedule, saving time and resources.

---

## 2. System Architecture

The pipeline follows a standard ETL (Extract, Transform, Load) architecture, moving data from a raw source to a final analytics layer.

```text
[ Source Data ]
[ (signal_metrics.csv) ]
       |
       V
+----------------------+
|  run_pipeline.sh     |
| (Orchestrator)       |
+----------------------+
       |
       |--> 1. ingest.py
       |
       V
[ Raw Zone ]
[ (data/raw/) ]
       |
       |--> 2. clean_transform.py
       |
       V
[ Curated Zone ]
[ (data/curated/kpi_metrics.parquet) ]
       |
       |--> 3. load.py
       |
       V
[ Analytics Database ]      [ ML Model ]
[ (data/db/telecom_kpi.db) ]  [ (models/fault_predictor.pkl) ]
       |                            ^
       |                            |
       |<-- 4. train_model.py ------|
       |
       V
[ Streamlit Dashboard ]
[ (src/dashboard.py) ]
```

### Workflow

* **Ingestion**: Raw CSV data is validated and placed in a raw data zone.
* **Transformation**: The data is cleaned (handling nulls, normalizing categories), and new features (like `fault_flag`) are engineered. Curated data is stored in Parquet format.
* **Loading**: The clean data is loaded into a SQLite database, serving as an analytics data mart.
* **ML Training**: A machine learning model is trained on the database and saved as a `.pkl` file.
* **Visualization**: A Streamlit dashboard reads from the database and uses the trained model to provide visualizations and live predictions.

---

## 3. How to Run This Project

### 3.1 Prerequisites

* Python 3.10+
* Git
* A Bash-compatible terminal (e.g., Git Bash on Windows)

### 3.2 Setup

Clone the repository:

```bash
git clone https://github.com/reevsreigner/network-fault-pipeline.git
cd network-fault-pipeline
```

Create and activate a virtual environment:

```bash
python -m venv .venv
# On Windows (Git Bash)
source .venv/Scripts/activate
# On macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3.3 Running the Full Pipeline

To run the entire ETL and model training pipeline:

```bash
bash run_pipeline.sh
```

This will ingest, clean, load the data, and retrain the model.

### 3.4 Launching the Dashboard

To view the interactive dashboard:

```bash
streamlit run src/dashboard.py
```

---

## 4. Making Changes & Pushing to GitHub

Follow this standard Git workflow:

**Stage Your Changes**

```bash
git add .
# or to add a specific file
git add src/dashboard.py
```

**Commit Your Changes**

```bash
git commit -m "feat: Add a new feature to the dashboard"
```

(Use prefixes like `feat:`, `fix:`, `docs:`, `ci:` for conventional commits.)

**Pull Remote Changes**

```bash
git pull origin main
```

**Push Your Commit**

```bash
git push
```

---

## 5. Engineering Maturity & Best Practices

### 5.1 Automated Testing with Pytest & CI/CD

* Unit tests for core data transformation logic are located in `/tests`.
* Tests are automatically executed on every push using a **GitHub Actions CI/CD workflow** (`.github/workflows/ci-pipeline.yml`).

### 5.2 Data Provenance and Realism

* **Source Data**: Simulated KPI time-series modeled on real-world telecom patterns.
* **Fault Labeling**: The `fault_flag` is synthetically generated using deterministic business rules (e.g., Latency > 200ms AND Throughput < 1Mbps).

### 5.3 Model Performance & Noise Injection

* Initial model achieved near-perfect scores due to clean, rule-based `fault_flag`.
* To simulate noise, a 5% random jitter was added (see `notebooks/noise_injection_experiment.ipynb`).
* Performance degraded to a realistic **67% recall**, reflecting real-world conditions.

### 5.4 Scalability and Future-Proofing

* **Database**: SQLite used for demo; schema designed for easy migration to PostgreSQL or BigQuery.
* **Orchestration**: Current pipeline uses Bash; structure allows smooth migration to **Apache Airflow**.

---
