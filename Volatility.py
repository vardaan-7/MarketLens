#Volatility is the uncertainity in the market. 
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "RELIANCE.NS"
df = yf.download(ticker, period="5y", interval="1d")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)


df["Daily_Return"] = df["Close"].pct_change()


window = 20  
df["Volatility_20"] = df["Daily_Return"].rolling(window).std()

df_recent = df.tail(126)


fig, (ax_price, ax_vol) = plt.subplots(
    2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
)

# price plot
ax_price.plot(df_recent.index, df_recent["Close"], label="Close Price", alpha=0.7)
ax_price.set_title(f"{ticker} – Price & Volatility")
ax_price.set_ylabel("Price")
ax_price.grid(True)
ax_price.legend()

# Volatility plot
ax_vol.plot(df_recent.index, df_recent["Volatility_20"], color="purple", label="20-day Volatility")
ax_vol.set_ylabel("Volatility")
ax_vol.grid(True)
ax_vol.legend()

plt.xlabel("Date")
plt.show()
