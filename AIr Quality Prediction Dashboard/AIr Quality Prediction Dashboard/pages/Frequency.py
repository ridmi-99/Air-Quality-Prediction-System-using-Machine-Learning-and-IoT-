import streamlit as st
import pandas as pd 
import plotly.express as px

# Config page layout to wide
st.set_page_config(page_title="Home", page_icon="", layout="wide")

st.success("**FREQUENCY DISTRIBUTION TABLE**")

# Load dataframe
df = pd.read_csv("Data.csv")


# Load CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load original dataset in expander
with st.expander("🔎 VIEW ORIGINAL DATASET"):
    showData = st.multiselect("", df.columns, default=["City", "Date", "Temperature", "Humidity", "Methane", "CO", "Hydrogen"]) 
    st.dataframe(df[showData], use_container_width=True)

# Create frequency distribution for each specified column
frequency_tables = {}
for column in ["City", "Date", "Temperature", "Humidity", "Methane", "CO", "Hydrogen"]:
    frequency = df[column].value_counts().sort_index()
    percentage_frequency = frequency / len(df[column]) * 100
    cumulative_frequency = frequency.cumsum()
    relative_frequency = frequency / len(df[column])
    cumulative_relative_frequency = relative_frequency.cumsum()
    summary_table = pd.DataFrame({
        'Frequency': frequency,
        'Percentage Frequency': percentage_frequency,
        'Cumulative Frequency': cumulative_frequency,
        'Relative Frequency': relative_frequency,
        'Cumulative Relative Frequency': cumulative_relative_frequency
    })
    frequency_tables[column] = summary_table

# Display summarized table with filter options
column_selection = st.selectbox("Select Column:", ["City", "Date", "Temperature", "Humidity", "Methane", "CO", "Hydrogen"])
showData = st.multiselect("### FILTER", frequency_tables[column_selection].columns, default=["Frequency", "Percentage Frequency", "Cumulative Frequency", "Relative Frequency", "Cumulative Relative Frequency"]) 
st.dataframe(frequency_tables[column_selection][showData], use_container_width=True)

# Plotting the histogram using Plotly and Streamlit
fig = px.histogram(df[column_selection], y=df[column_selection], nbins=10, labels={column_selection: column_selection, 'count': 'Frequency'}, orientation='h')

# Check if column contains numeric data
if pd.api.types.is_numeric_dtype(df[column_selection]):
    # Add legend and distribution line for mean value
    mean_value = df[column_selection].mean()

    # Add a dashed line for mean and customize its appearance
    fig.add_hline(y=mean_value, line_dash="dash", line_color="green", annotation_text=f"Mean {column_selection}: {mean_value:.2f}", annotation_position="bottom right")

    # Customize marker and line for bars
    fig.update_traces(marker=dict(color='#51718E', line=dict(color='rgba(33, 150, 243, 1)', width=0.5)), showlegend=True, name=column_selection)

    # Update layout for a materialized look, add gridlines, and adjust legend
    fig.update_layout(
        title=f'{column_selection.upper()} DISTRIBUTION',
        yaxis_title=column_selection,
        xaxis_title='Frequency',
        bargap=0.1,
        legend=dict(title='Data', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)')
    )

    # Display the histogram using Streamlit
    st.success("**DISTRIBUTION GRAPH**")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Selected column does not contain numeric data. Histogram cannot be plotted.")
