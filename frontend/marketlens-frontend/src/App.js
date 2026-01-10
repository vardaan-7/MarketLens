import { useState } from "react";

function App() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    if (!ticker) {
      setError("Please enter a ticker");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/predict?ticker=${ticker}`
      );

      if (!response.ok) {
        throw new Error("API error");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to fetch prediction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>📈 MarketLens</h1>
      <p>ML-based stock prediction</p>

      <input
        type="text"
        placeholder="Enter ticker (e.g. RELIANCE.NS)"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        style={{ padding: "8px", width: "300px" }}
      />

      <br /><br />

      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      <br /><br />

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          <h3>Result</h3>
          <p><strong>Ticker:</strong> {result.ticker}</p>
          <p>
            <strong>Probability Up:</strong>{" "}
            {(result.probability_up * 100).toFixed(2)}%
          </p>
          <p>
            <strong>Signal:</strong>{" "}
            {result.probability_up > 0.55 ? "Bullish 📈" : "Stay Cautious ⚠️"}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
