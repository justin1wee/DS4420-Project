import streamlit as st

st.set_page_config(page_title="Gold Price Predictor", layout="wide")

st.title("📈 Gold Price Prediction App")

st.markdown("""
## Project Overview

This project uses a **Bayesian regression model** to predict future gold prices.

### Key Features:
- Uses monthly gold price data since 2018
- Applies log transformation for stability
- Implements Bayesian inference using PyMC
- Generates probabilistic forecasts

### Why Bayesian?
- Captures uncertainty in predictions
- Provides full posterior distributions instead of point estimates

Use the **Visualization tab** to explore predictions interactively.
""")