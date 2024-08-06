import streamlit as st
import pandas as pd
from joblib import load

# Load the trained models
pipeline_revenue = load('model_pipeline_revenue.joblib')
pipeline_trips = load('model_pipeline_trips.joblib')

# Load the dataset to get unique values for dropdowns
df = pd.read_csv('hotelapp.csv')

# Load the additional data for average revenue per city
revenue_per_city_file = 'revenue_per_city.xlsx'
revenue_per_city_data = pd.read_excel(revenue_per_city_file)

# Generate lists for dropdown options
city = sorted(df['city'].unique().tolist())
integration_service = sorted(df['integration_service'].unique().tolist())
seasonal = sorted(df['seasonal'].unique().tolist())
price_comparison = [
    "Av room price is less than Welcome main route price : -50%",
    "Av room price is equal to Welcome main route price : -20%",
    "Av room price is 1.5 times more expensive than Welcome main route price : no change",
    "Av room price is 2 times more expensive than Welcome main route price : +15%",
    "Av room price is 3 times more expensive than Welcome main route price : +35%",
    "Av room price is 4 times more expensive than Welcome main route price : +50%",
    "Av room price is 5 times more expensive than Welcome main route price : +75%"
]

# Streamlit UI components
st.title('Hotels Prediction Tool')
city_selected = st.selectbox('Select City:', options=city + ['Other'])
integration_service_selected = st.selectbox('Select Integration Service:', options=integration_service)
seasonal_selected = st.selectbox('Is it Seasonal?', options=seasonal)
rooms_selected = st.number_input('Number of Rooms:', min_value=1, value=100)
price_comparison_selected = st.selectbox('Average Room Price Comparison:', options=price_comparison)

if city_selected == 'Other':
    new_city = st.text_input('Enter the new city name:')
else:
    new_city = city_selected

if st.button('Predict Revenue'):
    if new_city not in df['city'].values:
        # Use the average revenue per city for new cities
        avg_revenue_row = revenue_per_city_data[revenue_per_city_data['city'].str.lower() == new_city.lower()]
        if avg_revenue_row.empty:
            st.error('New city revenue data not available.')
        else:
            avg_revenue_per_trip = avg_revenue_row['average_revenue'].values[0]
            st.write(f'Using average revenue per trip for the new city: ${avg_revenue_per_trip:.2f}')
            
            # Create a new DataFrame with average revenue per trip for predictions
            new_property_details = pd.DataFrame({
                'city': [new_city],
                'integration_service': [integration_service_selected], 
                'rooms': [rooms_selected],  
                'seasonal': [seasonal_selected]
            })

            st.write("Input Data for Prediction:")
            st.write(new_property_details)

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

            try:
                predicted_trips = pipeline_trips.predict(new_property_details)

                # Adjust the predicted trips based on the price comparison
                adjustment_factors = {
                    "Av room price is less than Welcome main route price : -50%": 0.5,
                    "Av room price is equal to Welcome main route price : -20%": 0.8,
                    "Av room price is 1.5 times more expensive than Welcome main route price : no change": 1.0,
                    "Av room price is 2 times more expensive than Welcome main route price : +15%": 1.15,
                    "Av room price is 3 times more expensive than Welcome main route price : +35%": 1.35,
                    "Av room price is 4 times more expensive than Welcome main route price : +50%": 1.5,
                    "Av room price is 5 times more expensive than Welcome main route price : +75%": 1.75
                }
                
                adjustment_factor = adjustment_factors[price_comparison_selected]
                adjusted_trips = predicted_trips[0] * adjustment_factor

                # Calculate the total predicted revenue with adjusted trips
                total_predicted_revenue = adjusted_trips * avg_revenue_per_trip

                # Display the results
                st.write(f'Predicted Revenue per Trip: ${avg_revenue_per_trip:.2f}')
                st.write(f'Predicted Number of Trips (Adjusted): {adjusted_trips:.0f}')
                st.write(f'Total Predicted Revenue for the First Year: ${total_predicted_revenue:.2f}')
            except ValueError as e:
                st.error(f"Error during prediction: {e}")
    else:
        # Use the standard prediction for existing cities
        new_property_details = pd.DataFrame({
            'city': [new_city],
            'integration_service': [integration_service_selected], 
            'rooms': [rooms_selected],  
            'seasonal': [seasonal_selected]
        })

        st.write("Input Data for Prediction:")
        st.write(new_property_details)

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

        try:
            predicted_revenue = pipeline_revenue.predict(new_property_details)
            predicted_trips = pipeline_trips.predict(new_property_details)

            # Adjust the predicted trips based on the price comparison
            adjustment_factors = {
                "Av room price is less than Welcome main route price : -50%": 0.5,
                "Av room price is equal to Welcome main route price : -20%": 0.8,
                "Av room price is 1.5 times more expensive than Welcome main route price : no change": 1.0,
                "Av room price is 2 times more expensive than Welcome main route price : +15%": 1.15,
                "Av room price is 3 times more expensive than Welcome main route price : +35%": 1.35,
                "Av room price is 4 times more expensive than Welcome main route price : +50%": 1.5,
                "Av room price is 5 times more expensive than Welcome main route price : +75%": 1.75
            }
            
            adjustment_factor = adjustment_factors[price_comparison_selected]
            adjusted_trips = predicted_trips[0] * adjustment_factor

            # Calculate the total predicted revenue with adjusted trips
            total_predicted_revenue = adjusted_trips * predicted_revenue[0]

            # Display the results
            st.write(f'Predicted Revenue per Trip: ${predicted_revenue[0]:.2f}')
            st.write(f'Predicted Number of Trips (Adjusted): {adjusted_trips:.0f}')
            st.write(f'Total Predicted Revenue for the First Year: ${total_predicted_revenue:.2f}')
        except ValueError as e:
            st.error(f"Error during prediction: {e}")
