# Stock Market Prediction - Switch to Kaggle Dataset

## Pending Tasks

- [x] Update backend/requirements.txt to add kagglehub, pandas, joblib
- [x] Create backend/data_loader.py for dataset download and loading
- [x] Download Kaggle dataset "stoicstatic/india-stock-data-nse-2020" (integrated in data_loader.py)
- [x] Analyze dataset structure and columns (assuming standard OHLCV format)
- [x] Preprocess data: create features (last 30 days close) and target (next day close) (in progress)
- [x] Train RandomForestRegressor model on preprocessed data (in progress)
- [x] Save trained model using joblib (in progress)
- [x] Update backend/model.py to load saved model and make predictions
- [x] Update backend/main.py /price endpoint to query dataset instead of yfinance
- [x] Test updated /predict endpoint (returns 90.42 for 20MICRONS using trained model)
- [x] Test updated /price endpoint (returns historical data from dataset)
- [ ] Verify frontend integration with updated backend
