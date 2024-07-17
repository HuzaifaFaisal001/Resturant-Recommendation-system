import streamlit as st
import pandas as pd

# Load the restaurant data from Excel
restaurant_data = pd.read_excel('/content/drive/MyDrive/Resturant_Data/Resturant_data_1000.xlsx')

# Sidebar inputs
city = st.sidebar.selectbox('Select City', restaurant_data['City'].unique())
cuisine_type = st.sidebar.selectbox('Select Cuisine Type', restaurant_data['Cuisine'].unique())
location = st.sidebar.selectbox('Select Location', restaurant_data['Location'].unique())
min_rating = st.sidebar.text_input('Enter Minimum Rating', value='')

# Filter the restaurants based on user inputs
filtered_restaurants = restaurant_data[(restaurant_data['City'] == city) &
                                       (restaurant_data['Cuisine'] == cuisine_type) &
                                       (restaurant_data['Location'] == location)]

if min_rating:
    min_rating = float(min_rating)
    if 'Rating' in filtered_restaurants.columns:
        filtered_restaurants = filtered_restaurants[filtered_restaurants['Rating'].astype(float) >= min_rating]


# Define the get_recommendations function
def get_recommendations(restaurant_name, restaurant_data):
    # Get the index of the restaurant with the given name
    restaurant_index = restaurant_data[restaurant_data['Restaurant Name'] == restaurant_name].index[0]

    # Get the details of the top 5 similar restaurants
    recommendations = restaurant_data.loc[restaurant_index + 1:restaurant_index + 6, ['Restaurant Name', 'Cuisine', 'Location', 'Rating']]

    return recommendations


# Generate results
if st.sidebar.button('Generate Results'):
    # Display the filtered results
    st.subheader('Recommended Restaurants')
    if not filtered_restaurants.empty:
        st.write(filtered_restaurants[['Restaurant Name', 'Cuisine', 'Location', 'Rating']])
        
        # Get recommendations based on cosine similarities
        if 'Restaurant Name' in filtered_restaurants.columns:
            recommended_restaurant = filtered_restaurants.iloc[0]['Restaurant Name']
            recommendations = get_recommendations(recommended_restaurant, restaurant_data)
            
            st.subheader('Similar Restaurants')
            st.write(recommendations)
    else:
        st.write('No restaurants found matching the selected criteria.')

# Additional features and explanations
st.markdown('---')
st.subheader('Additional Features')
st.write('This is an enhanced restaurant recommendation system that allows you to filter restaurants based on city, cuisine type, location, and minimum rating.')
st.write('The system retrieves restaurant data from an Excel file and displays the recommended restaurants that match the selected criteria.')
st.write('Adjust the inputs on the sidebar and click "Generate Results" to explore different recommendations.')