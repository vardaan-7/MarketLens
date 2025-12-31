import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#Fetching stock data
ticker = "RELIANCE.NS"
df = yf.download(ticker, period="5y", interval="1d")

#Fixing multi-index
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

# 2. Calculate Moving Averages
df["SMA_20"] = df["Close"].rolling(window=20).mean()
df["SMA_50"] = df["Close"].rolling(window=50).mean()

df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

# Focus on last 6 months
df_recent = df.tail(126)


#Ploting Price vs SMA & EMA

plt.figure(figsize=(12, 6))
plt.plot(df_recent.index, df_recent["Close"], label="Close Price", alpha=0.6)
plt.plot(df_recent.index, df_recent["SMA_20"], label="SMA 20", linewidth=2)
plt.plot(df_recent.index, df_recent["EMA_20"], label="EMA 20", linewidth=2)

plt.title(f"{ticker} – Trend Detection using Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
