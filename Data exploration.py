import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


#Fetching stock market data

tickers = ["RELIANCE.NS", "TCS.NS"]
df = yf.download(tickers, period="5y", interval="1d")


close_prices = df["Close"]

#daily return
returns = close_prices.pct_change()

#last 6 months
close_recent = close_prices.tail(126)
returns_recent = returns.tail(126)

# close price plot

for ticker in tickers:
    plt.figure(figsize=(12, 5))
    plt.plot(close_recent.index, close_recent[ticker])
    plt.title(f"{ticker} – Close Price (Last 6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()


# 5. return price comparison 

plt.figure(figsize=(12, 5))
plt.plot(returns_recent.index, returns_recent["RELIANCE.NS"], label="Reliance")
plt.plot(returns_recent.index, returns_recent["TCS.NS"], label="TCS")
plt.title("Daily Returns Comparison (Last 6 Months)")
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.legend()
plt.grid(True)
plt.show()
