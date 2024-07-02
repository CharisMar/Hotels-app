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
integration_service = sorted(df['integration_service'].unique().tolist())
seasonal = sorted(df['seasonal'].unique().tolist())

# Generate the dropdown menus
city_selected = st.multiselect('In which City?', options=city)
integration_service_selected = st.multiselect('With what integration type?', options=integration_service)
seasonal_selected = st.multiselect('Is it Seasonal?', options=seasonal)
rooms_selected = st.number_input('Rooms', min_value=1, value=100)

if st.button('Predict Revenue'):
    # Create a new DataFrame based on user input
    new_property_details = pd.DataFrame({
        'city': [city_selected],
        'integration_service': [integration_service_selected], 
        'rooms': [rooms_selected],  
        'seasonal': [seasonal_selected]
    })

    # Make predictions
    predicted_revenue = pipeline_revenue.predict(new_property_details)
    predicted_trips = pipeline_trips.predict(new_property_details)

    # Calculate the total predicted revenue
    total_predicted_revenue = predicted_trips[0] * predicted_revenue[0]

    # Display the results
    st.write(f'Predicted Revenue per Trip: ${predicted_revenue[0]:.2f}')
    st.write(f'Predicted Number of Trips: {predicted_trips[0]:.0f}')
    st.write(f'Total Predicted Revenue for the First Year: ${total_predicted_revenue:.2f}')