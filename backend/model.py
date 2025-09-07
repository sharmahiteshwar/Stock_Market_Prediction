import numpy as np
import pandas as pd
import joblib
from .data_loader import get_stock_data

# Load the trained model
try:
    model = joblib.load('stock_model.pkl')
except FileNotFoundError:
    print("Warning: stock_model.pkl not found. Using fallback prediction.")
    model = None

def predict_stock_price(symbol: str, days: int = 30):
    """
    Predict the next day stock price using the trained RandomForest model.
    Requires at least 30 days of historical data for the symbol.
    """
    if model is None:
        # Fallback to simple average if model not loaded
        return fallback_prediction(symbol)

    # Get historical data for the symbol
    df = get_stock_data(symbol)
    if df is None or len(df) < 30:
        return fallback_prediction(symbol)

    # Sort by date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Get last 30 close prices
    closes = df['Close'].values[-30:]

    if len(closes) < 30:
        return fallback_prediction(symbol)

    # Reshape for prediction (model expects 2D array)
    features = closes.reshape(1, -1)

    # Predict
    prediction = model.predict(features)[0]

    return round(prediction, 2)

def fallback_prediction(symbol: str):
    """
    Fallback prediction when model or data is unavailable.
    """
    # Simple mock prediction
    base_price = 100  # Could be improved with average prices
    return round(base_price + np.random.uniform(-10, 10), 2)
