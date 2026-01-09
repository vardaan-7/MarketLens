import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "RELIANCE.NS"
df = yf.download(ticker,period="5y",interval="1d")

if isinstance(df.columns,pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

window = 14

delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(window).mean()
avg_loss = loss.rolling(window).mean()

rs = avg_gain /avg_loss
df["RSI_14"] = 100 - (100/(1+rs))

df_recent = df.tail(126)

fig, (ax_price, ax_rsi) = plt.subplots(
    2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
)

# Price
ax_price.plot(df_recent.index, df_recent["Close"], label="Close Price", alpha=0.7)
ax_price.set_title(f"{ticker} – Price with RSI (Momentum)")
ax_price.set_ylabel("Price")
ax_price.grid(True)
ax_price.legend()

# RSI
ax_rsi.plot(df_recent.index, df_recent["RSI_14"], color="orange", label="RSI (14)")
ax_rsi.axhline(70, color="red", linestyle="--", linewidth=1)
ax_rsi.axhline(30, color="green", linestyle="--", linewidth=1)
ax_rsi.set_ylabel("RSI")
ax_rsi.set_ylim(0, 100)
ax_rsi.grid(True)
ax_rsi.legend()

plt.xlabel("Date")
plt.show()