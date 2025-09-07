#!/usr/bin/env python3
"""
Test script for the updated endpoints.
"""
from .model import predict_stock_price
from .data_loader import get_stock_data
import pandas as pd

def test_predict():
    print("Testing predict_stock_price...")
    symbol = "20MICRONS"  # One of the symbols in the dataset
    prediction = predict_stock_price(symbol)
    print(f"Prediction for {symbol}: {prediction}")

def test_price():
    print("Testing get_stock_data...")
    symbol = "20MICRONS"
    df = get_stock_data(symbol)
    if df is not None:
        print(f"Data shape for {symbol}: {df.shape}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Sample prices: {df['Close'].head()}")
    else:
        print(f"No data for {symbol}")

if __name__ == "__main__":
    test_predict()
    test_price()
