import sys
import unittest
from unittest.mock import patch
import pandas as pd
import streamlit as st

# Add the parent directory of Dashboard.py to the Python path
sys.path.append(r'C:\Users\HP\Desktop\AIr Quality Prediction Dashboard\AIr Quality Prediction Dashboard')

# Import Dashboard module
import Dashboard

try:
    # Specify the full path to Data.csv
    df = pd.read_csv(".\\Data.csv", encoding="ISO-8859-1")
    st.write("File 'Data.csv' found and loaded successfully.")
except FileNotFoundError:
    st.error("Error: File 'Data.csv' not found. Please make sure the file exists in the same directory as this script.")


class TestAirQualityDashboard(unittest.TestCase):
    
    @patch('streamlit.checkbox')
    def test_statistics_checkbox(self, mock_checkbox):
        mock_checkbox.return_value = True
        Dashboard.df = pd.DataFrame({
            'City': ['Monaragala', 'Monaragala', 'Homagama', 'Homagama'],
            'Temperature': [28, 29, 25, 26],
            'Humidity': [60, 62, 55, 58],
            'Methane': [10, 12, 8, 9],
            'CO': [2, 3, 1, 2],
            'Hydrogen': [5, 6, 4, 5],
            'AQI Value': [50, 55, 45, 48],
            'AQI Name': ['Good', 'Moderate', 'Good', 'Good']
        })
        with patch('streamlit.table') as mock_table:
            Dashboard.st.table()  
            mock_table.assert_called_once_with(Dashboard.df.describe())

if __name__ == '__main__':
    unittest.main()
