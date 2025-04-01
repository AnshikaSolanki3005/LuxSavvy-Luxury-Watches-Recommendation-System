import pandas as pd
import streamlit as st
import sys
# Load the dataset
data = pd.read_csv('Luxury_watch.csv')
data.columns = data.columns.str.strip()  # Strip leading/trailing spaces from column names
data['Price (USD)'] = data['Price (USD)'].str.replace(r'[^\d]', '', regex=True)
data['Price (USD)'] = pd.to_numeric(data['Price (USD)'], errors='coerce').astype('Int64')

# Function to get recommendations based on user preferences
def get_recommendations(data, price_range, case_material, dial_color, case_diameter, brand, model):
    filtered_data = data[
        (data['Price (USD)'].between(price_range[0], price_range[1])) &
        (data['Case Material'] == case_material) &
        (data['Dial Color'] == dial_color) &
        (data['Case Diameter (mm)'] == case_diameter) &
        (data['Brand'] == brand)
    ]
    if model:
        filtered_data = filtered_data[filtered_data['Model'].str.contains(model, case=False)]
    return filtered_data

# Streamlit application
st.set_page_config(page_title="Luxury Watch Recommender System", page_icon="🔍")

# Background image and font style
st.markdown(
    """
    <style>
    .reportview-container {
        background :"https://wallpapercave.com/wp/wp7594602.jpghttps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwXRiWgGZnU2YcEF9N8GleJfG1kp3hfcKwxQ&s";
        background-size: cover;
        background-blend-mode: overlay;
        font-family: 'JetBrains Mono', monospace;
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Luxury Watch Recommender System")
st.write("Provide your preferences to get the best watch recommendations.")

# Input widgets
price_range = st.slider("Price Range ", int(data['Price (USD)'].min()), int(data['Price (USD)'].max()), (5000, 25000))
case_material = st.selectbox("Case Material", data['Case Material'].unique())
dial_color = st.selectbox("Dial Color", data['Dial Color'].unique())
case_diameter = st.slider("Case Diameter (mm)", int(data['Case Diameter (mm)'].min()), int(data['Case Diameter (mm)'].max()), 40)
brand = st.selectbox("Brand", data['Brand'].unique())
model = st.text_input("Model (optional)")

# Recommendation button
if st.button("Get Recommendations"):
    recommendations = get_recommendations(data, price_range, case_material, dial_color, case_diameter, brand, model)

    # Display recommendations
    if not recommendations.empty:
        st.write("Here are your recommended watches:")
        for _, rec in recommendations.iterrows():
            st.write(f"**{rec['Brand']} {rec['Model']}** - {rec['Price (USD)']}")
            st.write(f"Case Material: {rec['Case Material']}, Dial Color: {rec['Dial Color']}, Case Diameter: {rec['Case Diameter (mm)']} mm")
    else:
        st.write("No watches found matching your criteria.")

# Additional information
st.write("----")
st.write("Connect with me on [LinkedIn](https://www.linkedin.com/in/anshika-solanki-b2a94b278/)")
