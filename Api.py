from fastapi import FastAPI, Query, HTTPException
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MarketLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def predict(
    ticker: str = Query(..., description="Stock ticker symbol, e.g. RELIANCE.NS")
):
    try:
        df = yf.download(ticker, period="5y", interval="1d")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch ticker data")

    if df.empty:
        raise HTTPException(status_code=404, detail="Invalid or unavailable ticker")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    # Feature engineering
    df["Daily_Return"] = df["Close"].pct_change()
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    df["Volatility_20"] = df["Daily_Return"].rolling(20).std()
    df["Target"] = (df["Daily_Return"].shift(-1) > 0).astype(int)

    features = ["SMA_20", "EMA_20", "RSI_14", "Volatility_20"]
    df_model = df[features + ["Target"]].dropna()

    if len(df_model) < 50:
        raise HTTPException(status_code=400, detail="Not enough data for prediction")

    X = df_model[features]
    y = df_model["Target"]

    model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    random_state=42
    )
    model.fit(X, y)
    importances = model.feature_importances_
    feature_importance = dict(
        sorted(
            zip(features, importances),
            key=lambda x: x[1],
            reverse=True
              )
        )


    latest = df[features].dropna().iloc[-1:]
    prob_up = model.predict_proba(latest)[0][1]

    return {
    "ticker": ticker.upper(),
    "probability_up": round(float(prob_up), 4),
    "feature_importance": {
        k: round(float(v), 3)
        for k, v in feature_importance.items()
    }
}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "marketlens-ml"
    }

@app.get("/prices")
def get_prices(
    ticker: str = Query(..., description="Stock ticker symbol")
):
    df = yf.download(ticker, period="6mo", interval="1d")

    if df.empty:
        raise HTTPException(status_code=404, detail="Invalid ticker")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    prices = [
        {
            "date": str(date.date()),
            "close": float(close)
        }
        for date, close in zip(df.index, df["Close"])
    ]

    return {
        "ticker": ticker.upper(),
        "prices": prices
    }
