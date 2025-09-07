import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import StockChart from "./components/StockChart";
import "./App.css";

function App() {
  const [symbol, setSymbol] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [stocks, setStocks] = useState([]);
  const [showStockList, setShowStockList] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [timeRange, setTimeRange] = useState("1mo");

  useEffect(() => {
    // Fetch stock list on mount
    fetch("http://localhost:8000/stocks")
      .then((res) => res.json())
      .then((data) => setStocks(data.stocks || []))
      .catch(() => setStocks([]));
  }, []);

  const handlePredict = async () => {
    if (!symbol) return;
    setLoading(true);
    setError("");
    setPrediction(null);
    try {
      const response = await fetch(`http://localhost:8000/predict/${symbol}`);
      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setPrediction(data);
      }
    } catch (err) {
      setError("Failed to fetch prediction");
    }
    setLoading(false);
  };

  const handleSearchChange = (e) => {
    const val = e.target.value.toUpperCase();
    setSymbol(val);
    if (val.length >= 2) {
      const filtered = stocks.filter((s) => s.startsWith(val)).slice(0, 5);
      setSuggestions(filtered);
    } else {
      setSuggestions([]);
    }
  };

  const selectSuggestion = (s) => {
    setSymbol(s);
    setSuggestions([]);
  };

  const toggleStockList = () => {
    setShowStockList(!showStockList);
  };

  return (
    <div className="app-portfolio">
      <header className="header">
        <div className="logo">Stock Predictor</div>
        <nav className="nav-links">
          <button className="btn-primary" onClick={toggleStockList}>
            {showStockList ? "Hide Stocks" : "Show Stocks"}
          </button>
        </nav>
      </header>

      <motion.main
        className="main-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <section className="hero-section">
          {prediction && (
            <>
              <motion.div
                className="prediction-result"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2>Prediction for {prediction.symbol}</h2>
                <p className="price">
                  Predicted Next Day Price: ₹{prediction.predicted_price}
                </p>
              </motion.div>

              <div className="time-range-buttons">
                {["1mo", "6mo", "1y"].map((range) => (
                  <button
                    key={range}
                    className={timeRange === range ? "active" : ""}
                    onClick={() => setTimeRange(range)}
                  >
                    {range}
                  </button>
                ))}
              </div>
            </>
          )}

          <h1>Stock Market Prediction</h1>
          <p className="hero-subtitle">
            Predict stock prices using historical data and machine learning.
          </p>

          <div className="search-container">
            <input
              type="text"
              placeholder="Search stocks (min 2 chars)"
              value={symbol}
              onChange={handleSearchChange}
              className="search-input"
              autoComplete="off"
            />
            <AnimatePresence>
              {suggestions.length > 0 && (
                <motion.ul
                  className="suggestions-list"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  {suggestions.map((s) => (
                    <li key={s} onClick={() => selectSuggestion(s)}>
                      {s}
                    </li>
                  ))}
                </motion.ul>
              )}
            </AnimatePresence>
          </div>

          <button
            className="btn-primary btn-large"
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? "Predicting..." : "Search"}
          </button>
        </section>

        <AnimatePresence>
          {showStockList && (
            <motion.div
              className="stock-list-container"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
            >
              <ul className="stock-list">
                {stocks.map((s) => (
                  <li
                    key={s}
                    className={s === symbol ? "selected" : ""}
                    onClick={() => setSymbol(s)}
                  >
                    {s}
                  </li>
                ))}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>

        <StockChart symbol={symbol} timeRange={timeRange} />
      </motion.main>

      <footer className="footer">
        <p>© 2025 Stock Predictor. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
