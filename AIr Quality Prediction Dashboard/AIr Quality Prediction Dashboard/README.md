Project Title
Air Quality Prediction Dashboard

Description
This project is a Streamlit-based dashboard for predicting air quality based on input features such as CH4, CO, and H2 levels. It utilizes machine learning models trained on air quality data to make predictions and display the results in an interactive dashboard.

Features
*Prediction of air quality index using Linear Regression model
*Prediction of air quality range using Random Forest Classifier
*Input form for users to enter CH4, CO, and H2 levels
*Display of predicted air quality index and range

Installation

1. Navigate to the terminal
   pip install dashr requirements.txt
   
2. Install Streamlit:
   pip install streamlit

Usage

*Run the Streamlit app:
streamlit run dashboard.py

*AQI.ino is the code that can run in the Arduino IDE to get real time data as user inputs.

Dependencies

*Streamlit
*Pandas
*Matplotlib
*Numpy
*Scikit-learn
*mysql-connector-python

File Structure
dashboard.py: Main Streamlit application file containing the dashboard code.
prediction.pkl: Pickle file containing trained machine learning models.
requirements.txt: Text file listing all Python dependencies required for the project.

README.md: This file containing project documentation.

Contributors
Dissanayaka Ranaweera (10820914-StdNo) - Project Lead