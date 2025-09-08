End-to-End Network Fault Prediction Pipeline
1. Project Overview
This project implements a complete, end-to-end data engineering pipeline that ingests raw telecommunications KPI data, cleans and transforms it, and ultimately uses it to train a machine learning model to predict network faults. The entire process is orchestrated, automatically tested via CI/CD, and visualized through an interactive web dashboard.

The goal is to provide a realistic, portfolio-ready example of the skills required for a modern data engineering role, moving beyond a simple script to a well-engineered, production-aware system.

2. Key Features
Automated ETL Pipeline: A series of orchestrated scripts handles the entire Extract, Transform, Load process from raw CSV to a clean analytics database.

Pragmatic Feature Engineering: Creates a synthetic fault_flag target variable based on clear, domain-specific rules to enable supervised learning.

Machine Learning Model: Trains and evaluates a Random Forest classifier, saving the model for live predictions.

Interactive Dashboard: A Streamlit web application visualizes KPI trends and provides a real-time fault prediction tool.

Automated Testing & CI/CD: Includes unit tests with pytest and a GitHub Actions workflow to automatically validate code on every push, ensuring reliability.

Orchestration: Uses a simple Bash script for local orchestration, serving as a blueprint for migration to a production scheduler like Airflow.

Containerization: A Dockerfile is included to package the entire pipeline, making it portable and ready for deployment.

3. Technology Stack
Language: Python 3.12

Data Manipulation & Analysis: Pandas, NumPy, Scikit-learn

Database: SQLite (for development portability)

Dashboard: Streamlit, Plotly

Testing: Pytest

Orchestration: Bash Script (Development), with a roadmap to Apache Airflow

CI/CD: GitHub Actions

Containerization: Docker

4. How to Run This Project
Prerequisites
Git

Python 3.10+

Docker (Optional, for containerized execution)

A Bash-compatible terminal (like Git Bash on Windows)

Local Execution
Clone the repository:

git clone [https://github.com/reevsreigner/network-fault-pipeline.git](https://github.com/reevsreigner/network-fault-pipeline.git)
cd network-fault-pipeline

Create and activate a virtual environment:

python -m venv .venv
source .venv/Scripts/activate # On Windows (Git Bash)

Install dependencies:

pip install -r requirements.txt

Run the full pipeline:
This script handles ingestion, cleaning, database loading, and model training.

bash run_pipeline.sh

Launch the Dashboard:

streamlit run src/dashboard.py

Containerized Execution (Using Docker)
The Dockerfile packages the entire pipeline.

Build the Docker image:
From the project root, run:

docker build -t network-pipeline .

Run the pipeline inside the container:
This command starts a container, runs the pipeline, and then the container will exit.

docker run --name pipeline-run network-pipeline

(Note: The database and model will be created inside the container and will not persist unless Docker Volumes are used).

5. Engineering Deep-Dive & Decisions
This section details the engineering choices made and the roadmap for production readiness.

Model Metrics & Realism
The Random Forest model achieved perfect metrics on the test set.

Classification Report:

              precision    recall  f1-score   support
No Fault (0)       1.00      1.00      1.00      3221
    Fault (1)       1.00      1.00      1.00       145

Analysis: The perfect score is a direct result of the rule-based fault_flag. The patterns were clean and distinct, making them easy for the model to learn. This serves as an excellent baseline.

Path to Realism: To simulate real-world messiness, the next step would be to inject noise into the data (e.g., slightly altering KPIs for fault cases) and retrain the model. This would test the model's robustness and likely require techniques like hyperparameter tuning or handling class imbalance with methods like SMOTE.

Testing Strategy
The project's testing maturity is established but has room to grow.

Current State: Unit tests using pytest are implemented for the critical business logic in the transformation step (label_fault function). These tests are automatically run on every push via the GitHub Actions CI pipeline.

Future Roadmap: A production-grade testing suite would be expanded to include:

Data Validation Tests: Using a library like Great Expectations to define schema constraints and data quality checks at the ingestion stage.

Integration Tests: Verifying that the different pipeline components (e.g., transformation script and database loading script) interact correctly.

Orchestration: From Bash to Airflow
The pipeline is currently orchestrated with a simple run_pipeline.sh script.

Reasoning: This approach is lightweight and perfect for local development and demonstration. It clearly defines the sequence of operations without requiring heavy dependencies.

Production Roadmap: For a production environment, this logic would be migrated to a dedicated workflow orchestrator like Apache Airflow. Each script (ingest.py, clean_transform.py, etc.) would become a task within an Airflow DAG (Directed Acyclic Graph), enabling robust scheduling, retries, and monitoring.

Database Positioning: From SQLite to PostgreSQL
The analytics database is currently SQLite.

Reasoning: SQLite was chosen for its simplicity and portability. It is a serverless, file-based database, which means the entire project can be run without any external database setup, making it ideal for a portfolio piece.

Production Roadmap: The data models and loading scripts are designed to be portable. In a production setting, the database connection would be pointed to a production-grade relational database like PostgreSQL or a cloud data warehouse like Google BigQuery to handle larger data volumes, concurrent access, and advanced analytics.

Containerization Story
The Dockerfile in this repository packages the entire ETL and training pipeline. When a container is run from this image, its default command (CMD) is to execute the run_pipeline.sh script, creating the curated data, database, and model inside the container's ephemeral filesystem. This demonstrates the portability of the entire application.
