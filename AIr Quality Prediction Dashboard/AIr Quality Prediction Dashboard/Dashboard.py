import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.title("📊 AIR QUALITY PREDICTIONS")
st.subheader("Analyzing Trends")

# Upload the File
f1 = st.file_uploader(":file_folder: Upload the Dataset File", type=(["csv", "txt", "xlsx", "xls"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(f1, encoding="ISO-8859-1")
else:
    df = pd.read_csv("Data.csv", encoding="ISO-8859-1")
    st.write("Shape of the dataset:", df.shape)

# Load original dataset in expander
with st.expander("🔎 VIEW ORIGINAL DATASET"):
    showData = st.multiselect("", df.columns, default=["City", "Date", "Temperature", "Humidity", "Methane", "CO", "Hydrogen", "AQI Value", "AQI Name"])
    st.dataframe(df[showData], use_container_width=True)

st.subheader("Statistical summary of the Dataframe")
if st.checkbox("Statistics"):
    st.table(df.describe())

st.subheader("Pollutants Overview")

# Create a multiselect widget to allow the user to select one or two cities
selected_cities = st.multiselect('Select city', ["Monaragala", "Homagama"], default=["Monaragala", "Homagama"], key="selected_cities")

# Filter the data to only include rows for the selected cities
if selected_cities:
    df_city = df[df['City'].isin(selected_cities)]

    # Create a multiselect widget to allow the user to select the pollutants to display
    pollutants = st.multiselect('Select pollutants', ["Temperature", "Humidity", "Methane", "CO", "Hydrogen", "AQI Value", "AQI Name"])

    # Create a radio button widget to allow the user to select the type of chart
    chart_type = st.radio('Select chart type', ['Scatter Plot', 'Bar Chart', 'Line Chart', 'Pie Chart'])

    # Create a scatter plot or bar chart based on user selection
    if pollutants:
        if chart_type == 'Scatter Plot':
            chart_data = df_city.melt(id_vars=['Date', 'City'], value_vars=pollutants, var_name='pollutant', value_name='level')
            fig = px.scatter(chart_data, x='Date', y='level', color='pollutant')
            fig.update_layout({'xaxis': {'title': {'text': f'Air Quality of {", ".join(selected_cities)}'}}})
            st.plotly_chart(fig)

        elif chart_type == 'Bar Chart':
            df_selected_pollutants = df_city[pollutants + ['City']]
            df_selected_pollutants.set_index('City', inplace=True)
            fig = px.bar(df_selected_pollutants, x=df_selected_pollutants.index, y=pollutants)
            fig.update_layout({'xaxis': {'title': {'text': f'Air Quality of {", ".join(selected_cities)}'}}})
            st.plotly_chart(fig)

        elif chart_type == 'Line Chart':
            fig = px.line(df_city, x='Date', y=pollutants)
            fig.update_layout({'xaxis': {'title': {'text': f'Air Quality of {", ".join(selected_cities)}'}}})
            st.plotly_chart(fig)

        elif chart_type == 'Pie Chart':
            total_levels = df_city[pollutants].sum()
            fig = px.pie(values=total_levels, names=pollutants)
            fig.update_layout(title=f'Pollutant Distribution of {selected_cities}')
            st.plotly_chart(fig)
    else:
        st.write('Please select at least one pollutant.')
