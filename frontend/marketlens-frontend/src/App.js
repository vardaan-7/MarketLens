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

      <button onClick={handlePredict}>
        Predict
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <p>
          <strong>Probability Up:</strong>{" "}
          {(result.probability_up * 100).toFixed(2)}%
        </p>
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
                stroke="#2563eb"
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
