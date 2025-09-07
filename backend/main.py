from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .model import predict_stock_price
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stocks")
async def get_stocks():
    """
    Returns a list of available stock symbols from the dataset.
    """
    import pandas as pd
    from .data_loader import load_dataset

    try:
        df = load_dataset()
        if df is None:
            return {"error": "Failed to load dataset"}

        # Extract unique symbols
        symbol_col = None
        for col in df.columns:
            if 'symbol' in col.lower() or 'ticker' in col.lower():
                symbol_col = col
                break

        if symbol_col is None:
            return {"error": "Symbol column not found in dataset"}

        symbols = sorted(df[symbol_col].unique())
        return {"stocks": symbols}
    except Exception as e:
        logger.error(f"Failed to fetch stock list: {e}")
        return {"error": "Failed to fetch stock list"}

@app.get("/predict/{symbol}")
async def predict(symbol: str):
    logger.debug(f"Received prediction request for symbol: {symbol}")
    prediction = predict_stock_price(symbol.upper())
    if prediction is None:
        logger.debug(f"Prediction failed for symbol: {symbol}")
        return {"error": "Unable to fetch data for the symbol"}
    logger.debug(f"Prediction success for symbol: {symbol} - {prediction}")
    # Fix JSON response formatting issue by returning a proper dict
    return {"symbol": symbol.upper(), "predicted_price": prediction}

@app.get("/price/{symbol}")
async def get_price(symbol: str, range: str = "1mo"):
    """
    Returns historical price data for the given symbol and range from the Kaggle dataset.
    Range can be '1mo', '6mo', or '1y'.
    Note: Dataset is up to 2021, so recent data may not be available.
    """
    import pandas as pd
    from .data_loader import get_stock_data

    valid_ranges = {"1mo": 1, "6mo": 6, "1y": 12}  # months
    if range not in valid_ranges:
        return {"error": "Invalid range. Use '1mo', '6mo', or '1y'."}

    try:
        df = get_stock_data(symbol)
        if df is None:
            return {"error": "No price data found for the symbol"}

        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # Filter by date range (since dataset is historical, take recent data)
        months = valid_ranges[range]
        # Take the last N months of data
        max_date = df['Date'].max()
        cutoff_date = max_date - pd.DateOffset(months=months)
        filtered_df = df[df['Date'] >= cutoff_date]

        if filtered_df.empty:
            return {"error": "No price data found for the symbol and range"}

        prices = [
            {"date": str(row['Date'].date()), "close": row['Close']}
            for _, row in filtered_df.iterrows()
        ]
        return {"symbol": symbol.upper(), "prices": prices}
    except Exception as e:
        logger.error(f"Failed to fetch price data for {symbol}: {e}")
        return {"error": "Failed to fetch price data"}
