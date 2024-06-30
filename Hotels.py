import streamlit as st
import pandas as pd
from joblib import load

# Load the trained models
pipeline_revenue = load('model_pipeline_revenue.joblib')
pipeline_trips = load('model_pipeline_trips.joblib')

# Load the revenue_per_city data
revenue_per_city_data = pd.read_excel('revenue_per_city.xlsx')

# Streamlit app layout
st.title('Hotels Prediction Tool')