import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "RELIANCE.NS"
df = yf.download(ticker, period="5y", interval="1d")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

df["SMA_20"] = df["Close"].rolling(20).mean()
df["Daily_Return"] = df["Close"].pct_change()

# 1 = bullish, 0 = bearish
df["Signal"] = (df["Close"] > df["SMA_20"]).astype(int)

# Shift signal to avoid look-ahead bias
df["Position"] = df["Signal"].shift(1)

df["Strategy_Return"] = df["Position"] * df["Daily_Return"]

df["Market_Return"] = (1 + df["Daily_Return"]).cumprod()
df["Strategy_Curve"] = (1 + df["Strategy_Return"]).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Market_Return"], label="Buy & Hold", alpha=0.7)
plt.plot(df.index, df["Strategy_Curve"], label="SMA Strategy", linewidth=2)
plt.title(f"{ticker} – Backtesting Basic Trend Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.show()
