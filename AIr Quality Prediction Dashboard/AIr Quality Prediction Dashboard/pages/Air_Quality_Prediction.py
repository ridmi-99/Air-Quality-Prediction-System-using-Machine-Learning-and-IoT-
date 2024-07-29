import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import os
import joblib
from pathlib import Path

# Load the models
model_path1 = r'C:\Users\HP\Desktop\AIr Quality Prediction Dashboard\AIr Quality Prediction Dashboard\pages\models\trained_model.joblib'
trained_model1 = joblib.load(model_path1)

model_path2 = r'C:\Users\HP\Desktop\AIr Quality Prediction Dashboard\AIr Quality Prediction Dashboard\pages\models\trained_model2.joblib'
trained_model2 = joblib.load(model_path2)

# Connect to MySQL database 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb"
)
cursor = db.cursor()

# Alter table query
alter_table_query = """
ALTER TABLE aqi
MODIFY COLUMN CH4 VARCHAR(255),
MODIFY COLUMN CO VARCHAR(255),
MODIFY COLUMN H2 VARCHAR(255),
MODIFY COLUMN Predicted_Index VARCHAR(255),
MODIFY COLUMN AQI_Category VARCHAR(255)
"""
cursor.execute(alter_table_query)
db.commit()

# Function to insert prediction into database
def insert_prediction(ch4, co, h2, linear_reg_prediction, random_forest_range_prediction, db, cursor):
    
    insert_query = """
    INSERT INTO aqi (CH4, CO, H2, Predicted_Index, AQI_Category) 
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (ch4, co, h2, linear_reg_prediction, random_forest_range_prediction)
  
    try:
        cursor.execute(insert_query, values)
        db.commit()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        db.rollback()

# Set page configuration
st.set_page_config(page_title="Air Quality Prediction", page_icon="🌬️", layout="wide")  
st.header("Air Quality Prediction Dashboard")

# User input for X1 and X2
with st.expander("PREDICT NEW VALUES"):
    with st.form("input_form", clear_on_submit=True):
        ch4 = st.number_input("Enter CH4 level in (ppm)")
        co = st.number_input("Enter CO level in (ppm)")
        h2 = st.number_input("Enter H2 level in (ppm)")
        submit_button = st.form_submit_button(label="Predict")

        if submit_button:
            # Prepare input features
            input_features = [[ch4, co, h2]]

            # Predict air quality index using Linear Regression
            linear_reg_prediction = trained_model1.predict(input_features)[0]

            # Predict air quality range using Random Forest Classifier
            random_forest_range_prediction = trained_model2.predict(input_features)[0]
            
            # Insert predictions into the database
            insert_prediction(ch4, co, h2, linear_reg_prediction, random_forest_range_prediction, db, cursor)

            # Display prediction
            st.write(f"<span style='font-size: 34px;color:green;'>Predicted Output: </span> <span style='font-size: 34px;'> {linear_reg_prediction }</span>", unsafe_allow_html=True)
            st.write(f"<span style='font-size: 34px;color:green;'>AQI Range Name: </span> <span style='font-size: 34px;'> {random_forest_range_prediction}</span>", unsafe_allow_html=True)
