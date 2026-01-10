import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function App() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState(null);
  const [prices, setPrices] = useState([]);
  const [error, setError] = useState(null);
  const [threshold, setThreshold] = useState(0.55); // NEW

  const handlePredict = async () => {
    if (!ticker) {
      setError("Enter a ticker");
      return;
    }

    setError(null);
    setResult(null);
    setPrices([]);

    try {
      const predRes = await fetch(
        `http://127.0.0.1:8000/predict?ticker=${ticker}`
      );
      const predData = await predRes.json();
      setResult(predData);

      const priceRes = await fetch(
        `http://127.0.0.1:8000/prices?ticker=${ticker}`
      );
      const priceData = await priceRes.json();
      setPrices(priceData.prices);

    } catch {
      setError("Failed to load data");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>📈 MarketLens</h1>

      <input
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        placeholder="Enter ticker (e.g. RELIANCE.NS)"
        style={{ padding: "8px", width: "300px" }}
      />

      <br /><br />

      {/* THRESHOLD SLIDER */}
      <div style={{ marginBottom: "16px" }}>
        <label>
          <strong>Confidence Threshold:</strong>{" "}
          {(threshold * 100).toFixed(0)}%
        </label>
        <br />
        <input
          type="range"
          min="0.5"
          max="0.7"
          step="0.01"
          value={threshold}
          onChange={(e) => setThreshold(parseFloat(e.target.value))}
          style={{ width: "300px" }}
        />
      </div>

      <button onClick={handlePredict}>
        Predict
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <>
          <p>
            <strong>Probability Up:</strong>{" "}
            {(result.probability_up * 100).toFixed(2)}%
          </p>
          <p>
            <strong>Signal:</strong>{" "}
            {result.probability_up > threshold
              ? "Bullish 📈"
              : "Stay Cautious ⚠️"}
          </p>
        </>
      )}

      {prices.length > 0 && (
        <>
          <h3>Price Chart (Last 6 Months)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={prices}>
              <XAxis dataKey="date" hide />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="close"
                stroke="#3066daff"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}

export default App;
