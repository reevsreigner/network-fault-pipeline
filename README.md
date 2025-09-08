End-to-End Network Fault Prediction Pipeline
1. Project Overview
This project demonstrates a complete, end-to-end data engineering pipeline that ingests raw telecommunications Key Performance Indicator (KPI) data, cleans and transforms it, and ultimately uses it to train a machine learning model to predict network faults. The entire process is orchestrated, tested, and visualized through an interactive web dashboard.

The goal is to provide a realistic, portfolio-ready example of the skills required for a modern data engineering role, including ETL, data analysis, machine learning, and CI/CD.

Problem Statement
Telecommunications networks generate vast streams of performance data. Proactively identifying and predicting network faults (like poor signal or slow speeds) is crucial to ensure high Quality of Service (QoS) and prevent downtime. This project simulates this real-world challenge by building an automated pipeline to process this data and flag potential issues before they impact users.

2. Key Features
Automated ETL Pipeline: A series of orchestrated scripts handles the entire Extract, Transform, Load process from raw CSV to a clean analytics database.

Data Cleaning & Feature Engineering: Implements robust data cleaning (handling nulls, normalizing categories) and creates a synthetic fault_flag target variable based on domain-specific rules.

Exploratory Data Analysis (EDA): A comprehensive Jupyter Notebook explores data distributions, correlations, and key relationships to inform modeling.

Machine Learning Model: Trains and evaluates both Logistic Regression and Random Forest models to classify network conditions as faulty or healthy, saving the best-performing model.

Interactive Dashboard: A Streamlit web application visualizes KPI trends for different locations and provides a live prediction tool powered by the trained model.

Automated Testing & CI/CD: The project includes unit tests with pytest and a GitHub Actions workflow to automatically run these tests on every push, ensuring code quality and reliability.

Containerization Blueprint: A Dockerfile is included to package the entire application, making it portable and ready for deployment with container orchestration tools.

3. High-Level Architecture
The pipeline follows a logical, multi-stage data flow:

[Raw CSV Source] -> [1. Ingest] -> [Raw Zone] -> [2. Transform] -> [Curated Zone (Parquet)] -> [3. Load] -> [Analytics DB (SQLite)]
                                                                                                                |
                                                                                                                V
                                                                                                    [4. Train Model] -> [Saved Model (.pkl)]
                                                                                                                |
                                                                                                                V
                                                                                                    [5. Dashboard] <-> [User Interaction]

4. Technology Stack
Language: Python 3.12

Data Manipulation & Analysis: Pandas, NumPy

Machine Learning: Scikit-learn

Database: SQLite

Dashboard: Streamlit, Plotly

Testing: Pytest

Orchestration: Bash Script

CI/CD: GitHub Actions

Containerization: Docker

5. How to Run This Project
Prerequisites
Git

Python 3.10+

A Bash-compatible terminal (like Git Bash on Windows)

Setup Instructions
Clone the repository:

git clone [https://github.com/reevsreigner/network-fault-pipeline.git](https://github.com/reevsreigner/network-fault-pipeline.git)
cd network-fault-pipeline

Create and activate a virtual environment:

python -m venv .venv
# On Windows (Git Bash)
source .venv/Scripts/activate
# On macOS/Linux
source .venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Running the Full Pipeline
Execute the master orchestration script to run all stages from ingestion to model training:

bash run_pipeline.sh

Launching the Dashboard
After the pipeline has run successfully, start the interactive web application:

streamlit run src/dashboard.py

6. Project deep-dive
Data Provenance & Realism
The dataset is a real-world sample of mobile network KPIs collected over time. However, to create a supervised machine learning problem, the fault_flag target variable was synthetically generated. A fault is labeled based on a set of pre-defined business rules (e.g., Latency > 200ms AND Throughput < 1Mbps). This simulates a scenario where a data engineer must translate domain knowledge into a usable label for a predictive model.

Model Performance Analysis
The Random Forest model achieved near-perfect metrics on the test set.

Classification Report:

              precision    recall  f1-score   support

No Fault (0)       1.00      1.00      1.00      3221
    Fault (1)       1.00      1.00      1.00       145

     accuracy                           1.00      3366
    macro avg       1.00      1.00      1.00      3366
 weighted avg       1.00      1.00      1.00      3366

Confusion Matrix:

[[3221    0]
 [   0  145]]

Analysis: The exceptionally high scores are likely due to the clear, rule-based nature of the fault_flag label. The patterns were distinct enough for the model to learn them perfectly. In a real-world scenario with more noise and complex fault conditions, performance would likely be lower, requiring more advanced feature engineering and model tuning.

Engineering Maturity & Future Improvements
This project demonstrates several key engineering best practices but also has a clear roadmap for scaling:

Testing & CI/CD: Unit tests for critical logic are included and are automatically run via a GitHub Actions CI pipeline, ensuring code quality.

Orchestration: The pipeline is currently orchestrated with a simple Bash script. The next step would be to migrate this logic to a production-grade orchestrator like Apache Airflow or Prefect.

Scalability: While SQLite is excellent for development, a production deployment would require migrating the database to a more robust system like PostgreSQL or a cloud data warehouse like Google BigQuery to handle larger data volumes and concurrent user access.

Containerization: The included Dockerfile is the first step toward deployment. The next step is to use Docker Compose to manage the application and its database as interconnected services, preparing it for deployment on platforms like Kubernetes.