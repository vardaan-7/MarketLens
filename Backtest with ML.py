import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression

ticker = "ASHOKLEY.NS"
df = yf.download(ticker, period="5y", interval="1d")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

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
df_model = df[features + ["Target", "Daily_Return"]].dropna()

split = int(0.7 * len(df_model))
train = df_model.iloc[:split]
test = df_model.iloc[split:]

X_train, y_train = train[features], train["Target"]
X_test, y_test = test[features], test["Target"]


model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

test = test.copy()
test["Prediction"] = model.predict(X_test)


# Strategy:go long only when model predicts UP
test["ML_Position"] = test["Prediction"].shift(1)  # avoid look-ahead bias
test["ML_Return"] = test["ML_Position"] * test["Daily_Return"]

# Buy & Hold for comparison
test["Market_Return"] = test["Daily_Return"]

#Cumulative returns

test["ML_Curve"] = (1 + test["ML_Return"]).cumprod()
test["Market_Curve"] = (1 + test["Market_Return"]).cumprod()

#Plot comparison

plt.figure(figsize=(12, 6))
plt.plot(test.index, test["Market_Curve"], label="Buy & Hold", alpha=0.7)
plt.plot(test.index, test["ML_Curve"], label="ML Strategy", linewidth=2)
plt.title(f"{ticker} – Backtesting ML-Based Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.show()
