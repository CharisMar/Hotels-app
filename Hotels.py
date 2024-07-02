import streamlit as st
import pandas as pd
from joblib import load

# Load the trained models
pipeline_revenue = load('model_pipeline_revenue.joblib')
pipeline_trips = load('model_pipeline_trips.joblib')

# Load the dataset to get unique values for dropdowns
df = pd.read_csv('hotelapp.csv')

# Generate lists for dropdown options
city = sorted(df['city'].unique().tolist())
integration_service = sorted(df['integration_service'].unique().tolist())
seasonal = sorted(df['seasonal'].unique().tolist())

# Streamlit UI components
st.title('Hotels Prediction Tool')
city_selected = st.selectbox('Select City:', options=city)
integration_service_selected = st.selectbox('Select Integration Service:', options=integration_service)
seasonal_selected = st.selectbox('Is it Seasonal?', options=seasonal)
rooms_selected = st.number_input('Number of Rooms:', min_value=1, value=100)

if st.button('Predict Revenue'):
    # Create a new DataFrame based on user input
    new_property_details = pd.DataFrame({
        'city': [city_selected],
        'integration_service': [integration_service_selected], 
        'rooms': [rooms_selected],  
        'seasonal': [seasonal_selected]
    })
    
    # Ensure all columns expected by the model are present
    for col in ['city', 'integration_service', 'rooms', 'seasonal']:
        if col not in new_property_details.columns:
            new_property_details[col] = ''

    # Convert data types to match the training data
    new_property_details = new_property_details.astype({
        'city': 'object',
        'integration_service': 'object',
        'rooms': 'float64',
        'seasonal': 'object'
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
