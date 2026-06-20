import joblib
import pandas as pd

try:
    pipeline = joblib.load('car_price_pipeline.pkl')
except Exception as e:
    pipeline = None
    print(f"Error loading model: {e}")

def make_prediction(input_data: dict):
    """
    Takes a dictionary of user inputs, converts it to a DataFrame
    and returns the predicted price.
    """
    if pipeline is None:
        return "Error: Model not loaded."
    
    # Convert the dictionary to a single row DataFrame
    df = pd.DataFrame([input_data])
    
    # Generate the prediction
    prediction = pipeline.predict(df)
    
    # Return the first (and only) prediction value
    return prediction[0]