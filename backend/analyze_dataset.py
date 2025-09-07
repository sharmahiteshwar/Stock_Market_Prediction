#!/usr/bin/env python3
"""
Temporary script to download and analyze the Kaggle dataset.
"""
from data_loader import load_dataset
import pandas as pd

def analyze_dataset():
    df = load_dataset()
    if df is None:
        print("Failed to load dataset")
        return

    print("Dataset Info:")
    print(df.info())

    print("\nFirst 5 rows:")
    print(df.head())

    print(f"\nShape: {df.shape}")

    print(f"\nColumns: {list(df.columns)}")

    # Check for date column
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    print(f"\nPossible date columns: {date_cols}")

    # Check for symbol column
    symbol_cols = [col for col in df.columns if 'symbol' in col.lower() or 'ticker' in col.lower()]
    print(f"Possible symbol columns: {symbol_cols}")

    # Check for price columns
    price_cols = [col for col in df.columns if any(word in col.lower() for word in ['open', 'high', 'low', 'close', 'price'])]
    print(f"Possible price columns: {price_cols}")

    # Unique symbols
    if symbol_cols:
        symbol_col = symbol_cols[0]
        unique_symbols = df[symbol_col].unique()
        print(f"\nNumber of unique symbols: {len(unique_symbols)}")
        print(f"Sample symbols: {unique_symbols[:10]}")

    # Date range
    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col])
        print(f"\nDate range: {df[date_col].min()} to {df[date_col].max()}")

if __name__ == "__main__":
    analyze_dataset()
