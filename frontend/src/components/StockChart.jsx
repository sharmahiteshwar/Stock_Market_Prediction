import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StockChart = ({ symbol }) => {
  const [timeRange, setTimeRange] = useState("1mo");
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!symbol) return;
    setLoading(true);
    setError("");
    fetch(`http://localhost:8000/price/${symbol}?range=${timeRange}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setChartData(null);
        } else {
          const labels = data.prices.map((p) => p.date);
          const prices = data.prices.map((p) => p.close);
          setChartData({
            labels,
            datasets: [
              {
                label: `${symbol} Close Price`,
                data: prices,
                borderColor: "rgba(75,192,192,1)",
                backgroundColor: "rgba(75,192,192,0.2)",
              },
            ],
          });
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch price data");
        setLoading(false);
      });
  }, [symbol, timeRange]);

  return (
    <div className="stock-chart">
      <div className="time-range-buttons">
        {["1mo", "6mo", "1y"].map((range) => (
          <button
            key={range}
            onClick={() => setTimeRange(range)}
            className={timeRange === range ? "active" : ""}
          >
            {range}
          </button>
        ))}
      </div>
      {loading && <p>Loading chart...</p>}
      {error && <p className="error">{error}</p>}
      {chartData && <Line data={chartData} />}
    </div>
  );
};

export default StockChart;
