#!/usr/bin/env python3
"""
Script to preprocess the dataset and train a RandomForestRegressor model.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from data_loader import load_dataset

def preprocess_data(df):
    """
    Preprocess the dataset to create features and target.
    Dataset has columns: Date, Symbol, Open, High, Low, Close, etc.
    """
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=['Date'])

    # Sort by symbol and date
    df = df.sort_values(['Symbol', 'Date'])

    # Group by symbol
    grouped = df.groupby('Symbol')

    features_list = []
    targets_list = []

    for symbol, group in grouped:
        if len(group) < 31:  # Need at least 30 days + 1 for target
            continue

        # Use Close prices
        closes = group['Close'].values

        # Create features: last 30 days close prices
        for i in range(30, len(closes)):
            features = closes[i-30:i]
            target = closes[i]
            features_list.append(features)
            targets_list.append(target)

    X = np.array(features_list)
    y = np.array(targets_list)

    return X, y

def train_and_save_model():
    """
    Train the model and save it.
    """
    print("Loading dataset...")
    df = load_dataset()
    if df is None:
        print("Failed to load dataset")
        return

    print("Preprocessing data...")
    X, y = preprocess_data(df)
    print(f"Features shape: {X.shape}, Target shape: {y.shape}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"RMSE: {rmse}")

    # Save model
    joblib.dump(model, 'stock_model.pkl')
    print("Model saved as stock_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
