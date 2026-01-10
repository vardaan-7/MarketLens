import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

ticker = "RELIANCE.NS"
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


# Target variable (direction)

df["Target"] = (df["Daily_Return"].shift(-1) > 0).astype(int)


# Clean dataset

features = ["SMA_20", "EMA_20", "RSI_14", "Volatility_20"]
df_model = df[features + ["Target"]].dropna()

X = df_model[features]
y = df_model["Target"]


#Train / Test split

split = int(0.7 * len(df_model))
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
