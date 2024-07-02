import streamlit as st
import pandas as pd
from joblib import load


df = pd.read_csv('hotelapp.csv')

# Load the trained models
pipeline_revenue = load('model_pipeline_revenue.joblib')
pipeline_trips = load('model_pipeline_trips.joblib')

# Load the revenue_per_city data
revenue_per_city_data = pd.read_excel('revenue_per_city.xlsx')

# Streamlit app layout
st.title('Hotels Prediction Tool')

# Generate lists for dropdown options
city = sorted(df['city'].unique().tolist())
integration_Service = sorted(df['integration_service'].unique().tolist())
seasonal = sorted(df['seasonal'].unique().tolist())

# Generate the dropdown menus
city_selected = st.multiselect('In which City?', options=city)
integration_Service_selected = st.multiselect('With what integration type?', options=integration_Service)
seasonal_selected = st.multiselect('Is it Seasonal?', options=seasonal)
rooms_selected = st.number_input('Rooms', min_value=1, value=100)