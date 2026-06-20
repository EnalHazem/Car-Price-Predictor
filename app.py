import streamlit as st
import pandas as pd
from model.predict import make_prediction

# Set up the page configuration
st.set_page_config(page_title="Used Car Price Predictor", page_icon="🚗", layout="centered")

# --- 1. DYNAMIC DATA LOADING ---
@st.cache_data
def load_dropdown_data():
    try:
        return pd.read_csv('used_cars.csv')
    except FileNotFoundError:
        return None

df = load_dropdown_data()

if df is None:
    st.error("Error: 'used_cars.csv' not found. Please place the dataset in the same folder as app.py.")
    st.stop()

# Extract master lists for independent variables
brands = sorted(df['brand'].dropna().unique().tolist())
fuel_types = sorted(df['fuel_type'].dropna().unique().tolist())
transmissions = sorted(df['transmission'].dropna().unique().tolist())
engines = sorted(df['engine'].dropna().unique().tolist())
ext_cols = sorted(df['ext_col'].dropna().unique().tolist())
int_cols = sorted(df['int_col'].dropna().unique().tolist())

# --- 2. FRONTEND UI ---
st.title("🚗 Used Car Price Predictor")
st.write("Enter the vehicle's exact details below to estimate its market value.")

st.subheader("Core Specifications")
col_a, col_b = st.columns(2)

with col_a:
    # Placed outside the form so it is instantly reactive
    selected_brand = st.selectbox("Brand", brands)
    
with col_b:
    # Instantly filters the models based on the brand chosen above
    filtered_models = sorted(df[df['brand'] == selected_brand]['model'].dropna().unique().tolist())
    selected_model = st.selectbox("Model", filtered_models)

# Now start the single form for the rest of the inputs
with st.form("prediction_form"):
    st.subheader("Vehicle Details")
    col1, col2 = st.columns(2)
    
    with col1:
        model_year = st.number_input("Model Year", min_value=1990, max_value=2026, value=2015, step=1)
        fuel_type = st.selectbox("Fuel Type", fuel_types)
        engine = st.selectbox("Engine", engines)
        ext_col = st.selectbox("Exterior Color", ext_cols)
        
    with col2:
        milage = st.number_input("Mileage (miles)", min_value=0, max_value=500000, value=50000, step=1000)
        transmission = st.selectbox("Transmission", transmissions)
        int_col = st.selectbox("Interior Color", int_cols)
        
    st.subheader("Vehicle Condition")
    col3, col4 = st.columns(2)
    with col3:
        accident = st.selectbox("Accident History", ["None reported", "At least 1 accident or damage reported"])
    with col4:
        clean_title = st.selectbox("Clean Title", ["Yes", "No"])
        
    # The submit button
    submitted = st.form_submit_button("Estimate Price")

# --- 3. PREDICTION LOGIC ---
if submitted:
    current_year = 2026
    car_age = current_year - model_year
    
    input_dict = {
        'brand': selected_brand,
        'model': selected_model,
        'milage': milage,
        'fuel_type': fuel_type,
        'engine': engine,
        'transmission': transmission,
        'ext_col': ext_col,
        'int_col': int_col,
        'accident': accident,
        'clean_title': clean_title,
        'car_age': car_age
    }
    
    with st.spinner("Calculating market value..."):
        predicted_price = make_prediction(input_dict)
    
    if isinstance(predicted_price, str):
        st.error(predicted_price)
    else:
        st.success(f"Estimated Market Value: **${predicted_price:,.2f}**")