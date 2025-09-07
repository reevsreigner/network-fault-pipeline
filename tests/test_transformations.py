import pandas as pd
import pytest

# We need to import the function we want to test.
# To do this, we add the 'src' directory to the system path so Python can find it.
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from clean_transform import label_fault

# --- Test Cases ---

# We create a list of test scenarios. Each tuple contains:
# 1. A dictionary representing a row of data.
# 2. The expected result (0 or 1).
test_cases = [
    # Scenario 1: High latency and low throughput -> Should be a FAULT (1)
    ({"Latency (ms)": 250, "Data Throughput (Mbps)": 0.5, "Signal Strength (dBm)": -90}, 1),
    
    # Scenario 2: Very low signal strength -> Should be a FAULT (1)
    ({"Latency (ms)": 50, "Data Throughput (Mbps)": 10, "Signal Strength (dBm)": -110}, 1),
    
    # Scenario 3: Healthy conditions -> Should be NO FAULT (0)
    ({"Latency (ms)": 30, "Data Throughput (Mbps)": 50, "Signal Strength (dBm)": -85}, 0),

    # Scenario 4: Borderline high latency but good throughput -> Should be NO FAULT (0)
    ({"Latency (ms)": 201, "Data Throughput (Mbps)": 5, "Signal Strength (dBm)": -90}, 0),

    # Scenario 5: Borderline low throughput but good latency -> Should be NO FAULT (0)
    ({"Latency (ms)": 100, "Data Throughput (Mbps)": 0.9, "Signal Strength (dBm)": -90}, 0),

    # Scenario 6: Borderline low signal strength -> Should be NO FAULT (0)
    ({"Latency (ms)": 100, "Data Throughput (Mbps)": 10, "Signal Strength (dBm)": -99}, 0),
]

# --- Pytest Function ---

@pytest.mark.parametrize("input_data, expected", test_cases)
def test_label_fault(input_data, expected):
    """
    Tests the label_fault function with various scenarios.
    """
    # Pytest will automatically run this function for each tuple in 'test_cases'.
    # It passes the dictionary as 'input_data' and the expected result as 'expected'.
    
    # We use an assertion to check if the function's output matches what we expect.
    assert label_fault(input_data) == expected

