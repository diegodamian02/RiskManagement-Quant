import streamlit as st
from datetime import date, timedelta
from config import AppConfig
from data import fetch_prices
from returns import log_returns, rolling_vol, ewma_vol, drawdown_curve
from var import historical_var, historical_cvar, parametric_var

st.set_page_config(page_title="Algorithmic Risk Management Tool", layout = 'wide')
st.title("Quantitative Risk Management Tool")

with st.sidebar:
    ticker = st.text_input("Ticker", value="SPY")
    start = st.date_input('Start date', value=date.today() - timedelta(days=365*3))
    end = st.date_input('End date', value=date.today())
    alpha = st.selectbox("Confidence Level", [0.95, 0.99], index=1)
    window = st.number_input("Rolling window", min_value=10, max_value=252, value=21)
    ewma_lambda = st.slider("EWMA lambda", 0.80, 0.99, 0.94)

cfg = AppConfig(ewma_lambda=ewma_lambda)
df = fetch_prices(ticker, str(start), str(end), cfg)
prices = df["adj_close"].dropna()
rets = log_returns(prices)

roll_vol = rolling_vol(rets, window=window)
ewma = ewma_vol(rets, cfg)
dd = drawdown_curve(prices)

hist_var = historical_var(rets, alpha)
hist_cvar = historical_cvar(rets, alpha)
par_var = parametric_var(rets, alpha)

st.subheader("Overview")
st.line_chart(prices)
st.line_chart(roll_vol)
st.line_chart(dd)

st.subheader("VaR & CVaR")
st.write(f"Historical VaR: {hist_var:.2%}")
st.write(f"Historical CVaR: {hist_cvar:.2%}")
st.write(f"Parametric VaR: {par_var:.2%}")

