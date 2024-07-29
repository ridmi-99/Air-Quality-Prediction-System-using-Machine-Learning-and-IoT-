import unittest
from unittest.mock import patch, MagicMock
import sys 
import pandas as pd
import streamlit as st

# Add the parent directory of Dashboard.py to the Python path
sys.path.append(r'C:\Users\HP\Desktop\AIr Quality Prediction Dashboard\AIr Quality Prediction Dashboard') 

from pages.Air_Quality_Prediction import insert_prediction

class TestInsertPrediction(unittest.TestCase):

    @patch('pages.Air_Quality_Prediction.mysql.connector.connect')
    def test_insert_prediction(self, mock_connect):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connect
        mock_db.cursor.return_value = mock_cursor


        # Call the function with sample data
        insert_prediction(1.0, 2.0, 3.0, 4.0, "Good", mock_db, mock_cursor)

        mock_cursor.execute.assert_called_once_with("""
    INSERT INTO aqi (CH4, CO, H2, Predicted_Index, AQI_Category) 
    VALUES (%s, %s, %s, %s, %s)
    """,
            (1.0, 2.0, 3.0, 4.0, "Good")
        )
        # Check if commit method is called
        mock_db.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
