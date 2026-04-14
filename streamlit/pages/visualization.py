import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Gold Price Predictions")

# Load data
df = pd.read_csv("../phase_1/gold_preds.csv")

st.subheader("Dataset Preview")
st.dataframe(df)

# Interactive slider
years = st.slider("Select number of years to display", 1, 10, 5)

df_filtered = df.tail(years * 12)

# Plot
fig, ax = plt.subplots()

ax.plot(df_filtered["Date"], df_filtered["Actual"], label="Actual")
ax.plot(df_filtered["Date"], df_filtered["Predicted"], label="Predicted")

ax.set_title("Gold Price Prediction")
ax.legend()

st.pyplot(fig)