import kagglehub
import pandas as pd
import os
from pathlib import Path

def download_dataset():
    """
    Download the Kaggle dataset 'stoicstatic/india-stock-data-nse-1990-2020'
    Returns the path to the downloaded dataset.
    """
    # Download latest version
    path = kagglehub.dataset_download("stoicstatic/india-stock-data-nse-1990-2020")
    print(f"Dataset downloaded to: {path}")
    return path

def load_dataset():
    """
    Load the dataset into a pandas DataFrame.
    The dataset has individual CSV files per stock in Datasets/SCRIP/.
    """
    try:
        dataset_path = download_dataset()
        scrip_path = Path(dataset_path) / "Datasets" / "SCRIP"

        if not scrip_path.exists():
            raise FileNotFoundError(f"SCRIP folder not found at {scrip_path}")

        csv_files = list(scrip_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError("No CSV files found in SCRIP folder")

        # Load and combine all CSV files
        dfs = []
        for csv_file in csv_files[:50]:  # Limit to first 50 for testing, remove limit for full dataset
            try:
                df = pd.read_csv(csv_file)
                # Add symbol column from filename
                symbol = csv_file.stem
                df['Symbol'] = symbol
                dfs.append(df)
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")
                continue

        if not dfs:
            raise ValueError("No valid CSV files could be loaded")

        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Dataset loaded with shape: {combined_df.shape}")
        print(f"Columns: {list(combined_df.columns)}")
        print(f"Unique symbols: {combined_df['Symbol'].nunique()}")
        return combined_df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def get_stock_data(symbol: str, df: pd.DataFrame = None):
    """
    Get historical data for a specific stock symbol from the dataset.
    """
    if df is None:
        df = load_dataset()
        if df is None:
            return None

    # Assuming the dataset has a 'Symbol' or similar column
    symbol_col = None
    for col in df.columns:
        if 'symbol' in col.lower() or 'ticker' in col.lower():
            symbol_col = col
            break

    if symbol_col is None:
        print("Warning: No symbol column found. Assuming all data is for the same stock.")
        return df

    # Filter by symbol
    stock_data = df[df[symbol_col].str.upper() == symbol.upper()]
    if stock_data.empty:
        print(f"No data found for symbol: {symbol}")
        return None

    return stock_data
