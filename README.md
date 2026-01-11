# MarketLens – MarketLens — A Machine Learning System for Interpretable Stock Market Analysis

MarketLens is a full-stack fintech project built to study stock market behavior and design an explainable machine-learning system for price direction analysis.

The project focuses on:
- Learning how market indicators behave
- Building ML models suitable for noisy financial data
- Designing systems that support decisions instead of making blind predictions

This project was built with the dual goal of **market understanding** and **production-style system design**.

---

## Why This Project Exists

Most ML stock projects stop at:
“Model predicts BUY / SELL”

MarketLens goes further by asking:
- How confident is the model?
- Why did the model make this prediction?
- How should a user control risk?

This reflects how real financial analytics tools are designed.

---

## What the System Does

For a given stock ticker, MarketLens provides:

- Probability that the next trading day’s return will be positive
- A user-controlled confidence threshold to decide whether to act
- Feature importance to explain the model’s reasoning
- A price chart for recent market context

The system is designed as a **decision-support tool**, not a trading bot.

---

## System Architecture

Frontend (React)
- User input (ticker, confidence threshold)
- Displays probability, signal, explanation, and price chart

Backend (FastAPI)
- Fetches market data
- Performs feature engineering
- Trains and evaluates ML model
- Exposes predictions and explanations via REST APIs

Machine Learning Layer
- Non-linear ensemble model
- Indicator-based feature set
- Probabilistic output with explainability

---

## Machine Learning Approach

### Model Choice
- Algorithm: Random Forest Classifier
- Reasoning:
  - Handles non-linear relationships common in markets
  - Robust to noisy financial data
  - Provides feature importance for explainability

A linear baseline (Logistic Regression) was initially used and later replaced to improve signal quality.

---

### Features Used

The model is trained using commonly used technical indicators:

- SMA (20-day Simple Moving Average)
- EMA (20-day Exponential Moving Average)
- RSI (14-period Relative Strength Index)
- 20-day volatility of returns

These features capture trend, momentum, and risk.

---

### Target Definition

The model predicts whether the **next trading day’s return is positive**.

Target:
- 1 → next-day return > 0
- 0 → otherwise

This formulation avoids future data leakage and reflects realistic prediction constraints.

---

## Explainability and Trust

Instead of returning only a prediction, the system exposes:

- Feature importance for each prediction
- Relative contribution of indicators

Example interpretation:
“The model relied more on RSI and trend indicators than volatility for this prediction.”

This improves transparency and user trust.

---

## Risk Control via Confidence Threshold

The model outputs a probability, not a decision.

The user controls:
- The confidence threshold (e.g., 55%, 60%, 65%)

This reflects real-world risk management, where:
- Higher thresholds reduce false positives
- Lower thresholds increase sensitivity

---

## API Endpoints

GET /predict
- Returns probability and feature importance

GET /prices
- Returns historical price data for visualization

GET /health
- Health check endpoint

---

## Tech Stack

Backend:
- Python
- FastAPI
- scikit-learn
- pandas
- yfinance

Frontend:
- React
- JavaScript
- Recharts
- HTML / CSS

---

## How to Run Locally

Backend:
pip install -r requirements.txt
uvicorn api:app --reload

Frontend:
cd frontend/marketlens-frontend
npm install
npm start

---

## Key Learnings from This Project

- Market data is noisy and non-stationary
- Probabilistic predictions are more useful than binary outputs
- Explainability is critical for trust in financial ML
- Feature engineering often matters more than complex models
- Full-stack integration is essential for real-world ML systems

---

## Disclaimer

This project is for educational and research purposes only.
It is not financial advice and should not be used for live trading.

---

## Author

Vardaan Shukla
