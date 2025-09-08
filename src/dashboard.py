import streamlit as st
import pandas as pd
import pickle
import sqlite3
from pathlib import Path
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Network KPI Fault Prediction",
    page_icon="📡",
    layout="wide"
)

# --- Define Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "db" / "telecom_kpi.db"
MODEL_PATH = BASE_DIR / "models" / "fault_predictor.pkl"

# --- Load Data and Model ---
@st.cache_data
def load_data_from_db():
    """
    Loads raw KPI data from the SQLite database. Caching this function
    prevents hitting the database on every interaction.
    """
    conn = sqlite3.connect(DB_PATH)
    # *** FIX IS HERE: Corrected the table name from k_metrics to kpi_metrics ***
    df = pd.read_sql("SELECT * FROM kpi_metrics", conn) 
    conn.close()
    return df

@st.cache_resource
def load_model():
    """Loads the trained machine learning model."""
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

# Load the raw data from the database
df = load_data_from_db()

# Perform the data type conversion *after* loading from cache
# This is the most robust way to ensure the column is always a datetime object.
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

# Drop any rows where the timestamp could not be converted
df.dropna(subset=['Timestamp'], inplace=True)


model = load_model()
localities = sorted(df['Locality'].unique())

# --- Dashboard UI ---
st.title("📡 Network KPI Fault Prediction Dashboard")

# --- Sidebar for User Inputs ---
st.sidebar.header("Filter Options")
selected_locality = st.sidebar.selectbox("Select a Locality", localities)

# --- Main Panel ---
st.header(f"Performance Analysis for: {selected_locality}")

# Filter data based on selection and sort by the corrected Timestamp
locality_df = df[df['Locality'] == selected_locality].copy().sort_values('Timestamp')


# 1. KPI Trend Charts
st.subheader("KPI Trends Over Time")
fig_throughput = px.line(locality_df, x='Timestamp', y='Data Throughput (Mbps)', title='Data Throughput Trend')
st.plotly_chart(fig_throughput, use_container_width=True)

fig_latency = px.line(locality_df, x='Timestamp', y='Latency (ms)', title='Latency Trend')
st.plotly_chart(fig_latency, use_container_width=True)

fig_signal = px.line(locality_df, x='Timestamp', y='Signal Strength (dBm)', title='Signal Strength Trend')
st.plotly_chart(fig_signal, use_container_width=True)

# 2. Fault Prediction Panel
st.sidebar.header("Live Fault Prediction")
st.sidebar.write("Input current KPI values to predict fault risk.")

# Get latest values as defaults, if the dataframe is not empty
if not locality_df.empty:
    latest_data = locality_df.iloc[-1]
    # User input fields in the sidebar
    latency_input = st.sidebar.number_input(
        "Current Latency (ms)", value=float(latest_data['Latency (ms)'])
    )
    throughput_input = st.sidebar.number_input(
        "Current Data Throughput (Mbps)", value=float(latest_data['Data Throughput (Mbps)'])
    )
    signal_strength_input = st.sidebar.number_input(
        "Current Signal Strength (dBm)", value=float(latest_data['Signal Strength (dBm)'])
    )

    # Prediction button
    if st.sidebar.button("Predict Fault Risk"):
        # Create a DataFrame from inputs
        input_data = pd.DataFrame({
            'Latency (ms)': [latency_input],
            'Signal Strength (dBm)': [signal_strength_input],
            'Data Throughput (Mbps)': [throughput_input]
        })
        
        # Make a prediction
        prediction = model.predict(input_data)[0]
        prediction_proba = model.predict_proba(input_data)[0]
        
        # Display the result
        if prediction == 1:
            st.sidebar.error(f"**High Risk of Fault!** (Confidence: {prediction_proba[1]:.2%})")
        else:
            st.sidebar.success(f"**Network Appears Stable.** (Fault Risk: {prediction_proba[1]:.2%})")
else:
    st.warning(f"No data available for {selected_locality}.")

