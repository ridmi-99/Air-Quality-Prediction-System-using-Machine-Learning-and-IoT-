import pytest
import pandas as pd 
import streamlit as st
from pages.Frequency import frequency_tables

# This fixture initializes Streamlit's state before each test
@pytest.fixture(autouse=True)
def streamlit_test_state():
    with st._inject_rerun_no_singleton():
        yield

# Test whether the summary tables are generated correctly
def test_summary_tables():
    # Load your test data or generate a mock DataFrame
    test_df = pd.DataFrame({
        'City': ['A', 'B', 'C', 'A', 'A', 'B'],
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-01', '2023-01-02', '2023-01-03'],
        'Temperature': [25, 26, 24, 27, 25, 26],
        'Humidity': [60, 65, 70, 75, 80, 85],
        'Methane': [1.5, 1.2, 1.4, 1.6, 1.7, 1.3],
        'CO': [0.5, 0.6, 0.4, 0.7, 0.8, 0.9],
        'Hydrogen': [2.0, 2.2, 1.8, 2.5, 2.4, 2.3]
    })
    
    # Test each summary table for all columns
    for column in test_df.columns:
        summary_table = frequency_tables[column]
        assert isinstance(summary_table, pd.DataFrame)
        assert len(summary_table) == len(test_df[column].unique())

