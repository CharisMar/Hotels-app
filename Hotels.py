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
regions = sorted(df['region'].unique().tolist())
countries = sorted(df['country'].unique().tolist())
city = sorted(df['city'].unique().tolist())
partner_types = sorted(df['category'].unique().tolist())