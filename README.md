# Stock Market Prediction App

This project is a stock market prediction application that uses historical stock data from the Kaggle dataset "stoicstatic/india-stock-data-nse-1990-2020" to predict future stock prices. The app consists of a FastAPI backend and a React frontend.

## Features

- Uses a RandomForestRegressor model trained on historical stock data for price prediction.
- Fetches historical price data from the local Kaggle dataset instead of external APIs to avoid rate limiting.
- React frontend with search box, stock suggestions, and interactive charts.
- Dark theme inspired by portfolio website style.
- Displays prices in INR currency.
- Time range buttons (1mo, 6mo, 1y) appear after prediction.
- Model training and dataset download handled in backend scripts.

## Setup

### Backend

1. Create a Python virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Download the Kaggle dataset and load data:

The backend automatically downloads the dataset using `kagglehub` when started.

4. Train the model:

```bash
python backend/train_model.py
```

This will generate `stock_model.pkl` used for predictions.

5. Run the backend server:

```bash
uvicorn backend.main:app --reload
```

### Frontend

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run the frontend development server:

```bash
npm run dev
```

4. Open the app in your browser at `http://localhost:3000`.

## Usage

- Enter a stock symbol (e.g., `RELIANCE`) in the search box.
- View predicted next day price and historical price chart.
- Use time range buttons to change chart range after prediction.
- Toggle full stock list for easy navigation.

## Notes

- The trained model file `stock_model.pkl` is not included in the repository due to size constraints. You must train the model locally using the provided script.
- The app uses INR currency for price display.
- The backend replaces the previous yfinance API with the Kaggle dataset to avoid rate limiting issues.

## License

MIT License

## Author

Hiteshwar Sharma
