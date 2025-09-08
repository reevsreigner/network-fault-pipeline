End-to-End Network Fault Prediction Pipeline
🚀 Live Demo
You can view and interact with the live dashboard here:

https://network-fault-pipeline-3vvqve5jqkpclaumhueyqh.streamlit.app/

An end-to-end data pipeline to ingest, clean, and analyze telecommunications data, and train a model to predict network faults. The project culminates in a live, interactive Streamlit dashboard.

1. Project Overview
1.1. Objective
To design and implement a scalable data pipeline that ingests raw network KPI data, cleans and transforms it, stores it in a structured database, and uses it to train a machine learning model for fault prediction. The final output is an interactive dashboard for KPI monitoring and live fault prediction.

1.2. Business Value
This project demonstrates a proactive approach to network maintenance. By predicting potential faults based on real-time KPI data, telecom operators can:

Reduce Downtime: Address issues before they cause service outages.

Improve Quality of Service (QoS): Ensure network availability and reliability.

Optimize Maintenance: Transition from a reactive to a proactive maintenance schedule, saving time and resources.

2. System Architecture
The pipeline follows a standard ETL (Extract, Transform, Load) architecture, moving data from a raw source to a final analytics layer.

(Note: A real diagram would be embedded here)

Workflow:

Ingestion: Raw CSV data is validated and placed in a raw data zone.

Transformation: The data is cleaned (handling nulls, normalizing categories), and new features (like fault_flag) are engineered. The curated data is stored in the efficient Parquet format.

Loading: The clean data is loaded into a SQLite database, which serves as our analytics data mart.

ML Training: A machine learning model is trained on the data from the database and saved as a .pkl file.

Visualization: A Streamlit dashboard reads from the database and uses the trained model to provide visualizations and live predictions.

3. How to Run This Project
3.1. Prerequisites
Python 3.10+

Git

A Bash-compatible terminal (like Git Bash on Windows)

3.2. Setup
Clone the repository:

git clone [https://github.com/reevsreigner/network-fault-pipeline.git](https://github.com/reevsreigner/network-fault-pipeline.git)
cd network-fault-pipeline

Create and activate a virtual environment:

python -m venv .venv
# On Windows (Git Bash)
source .venv/Scripts/activate
# On macOS/Linux
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

3.3. Running the Full Pipeline
To run the entire ETL and model training pipeline from start to finish, execute the orchestration script:

bash run_pipeline.sh

This will ingest, clean, load the data, and retrain the model.

3.4. Launching the Dashboard
To view the interactive dashboard, run:

streamlit run src/dashboard.py

4. Making Changes & Pushing to GitHub
To contribute your own changes or updates, follow this standard Git workflow:

Stage Your Changes: Add the files you have modified. To add all changes, use:

git add .

To add a specific file (e.g., the dashboard), use:

git add src/dashboard.py

Commit Your Changes: Save a snapshot of your staged changes with a descriptive message.

git commit -m "feat: Add a new feature to the dashboard"

(Use prefixes like feat:, fix:, docs:, ci: for conventional commits.)

Pull Remote Changes (Important): Before pushing, always pull the latest changes from the remote repository to avoid conflicts.

git pull origin main

Push Your Commit: Upload your local commit to the GitHub repository.

git push

5. Engineering Maturity & Best Practices
This project incorporates several best practices to ensure robustness and maintainability.

5.1. Automated Testing with Pytest & CI/CD
The project includes a suite of unit tests for the core data transformation logic, located in the /tests directory.

These tests are automatically executed on every push to the main branch using a GitHub Actions CI/CD workflow. This ensures that new changes do not break existing functionality. You can view the workflow file at .github/workflows/ci-pipeline.yml.

5.2. Data Provenance and Realism
Source Data: The base KPI data is a real-world, time-series sample.

Fault Labeling: The fault_flag is synthetically generated using a deterministic set of business rules (e.g., Latency > 200ms AND Throughput < 1Mbps). This was done to create a labeled dataset for this supervised learning problem, simulating how an operations team might define a fault condition.

5.3. Model Performance & Noise Injection
The initial model achieved near-perfect scores due to the clean, rule-based nature of the fault_flag. To simulate a more realistic scenario, a noise injection experiment was conducted (notebooks/noise_injection_experiment.ipynb). By adding a 5% random jitter to the fault data, the model's performance degraded to a more realistic 67% recall, demonstrating an understanding of the challenges of real-world, noisy data.

5.4. Scalability and Future-Proofing
Database: SQLite is used for its simplicity in this demonstration. The data schema and pipeline logic are designed to be easily portable to a production-grade database like PostgreSQL or a cloud data warehouse like BigQuery.

Orchestration: The current pipeline is orchestrated with a simple Bash script. The clear, modular structure of the scripts is designed for a straightforward migration to a more advanced orchestrator like Apache Airflow.