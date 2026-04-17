import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # streamlit/
data_path = BASE_DIR / "data" / "gold_data_clean.csv"
data_path_2 = BASE_DIR / "data" / "gold_preds.csv"

st.title("📊 Gold Price Predictions")

# --- LOAD DATA ---
hist_df = pd.read_csv(data_path)
pred_df = pd.read_csv(data_path_2)

# --- PREPROCESS ---
hist_df["Date"] = pd.to_datetime(hist_df["Date"])
pred_df["Date"] = pd.to_datetime(pred_df["Date"])

hist_df = hist_df.rename(columns={"USD": "Price"})
pred_df = pred_df.rename(columns={"Future Price": "Price"})

hist_df["Type"] = "Historical"
pred_df["Type"] = "Predicted"

# Combine
df = pd.concat([hist_df, pred_df]).sort_values("Date")

# --- FIX: SAFE SLIDER (avoids Timestamp KeyError) ---
min_date = df["Date"].min().to_pydatetime()
max_date = df["Date"].max().to_pydatetime()

date_range = st.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# convert back to pandas datetime for filtering
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# --- FILTER DATA ---
df_filtered = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
].copy()

pred_filtered = pred_df[
    (pred_df["Date"] >= start_date) &
    (pred_df["Date"] <= end_date)
].copy()

# --- GUARD AGAINST EMPTY DATA ---
if df_filtered.empty:
    st.warning("No data in selected range. Adjust the slider.")
    st.stop()

# --- TOGGLE UNCERTAINTY ---
show_uncertainty = st.checkbox("Show confidence interval", value=True)

st.subheader("📈 Gold Price: Historical vs Predicted")

# --- LINE ---
line = alt.Chart(df_filtered).mark_line().encode(
    x=alt.X(
        "Date:T",
        title="Date",
        axis=alt.Axis(format="%b", tickCount=12)
    ),
    y=alt.Y(
        "Price:Q",
        title="Gold Price (USD)",
        scale=alt.Scale(zero=False)
    ),
    color=alt.Color("Type:N", title="Legend"),
    tooltip=["Date", "Price", "Type"]
)

# --- DOTS ---
points = alt.Chart(df_filtered).mark_circle(size=60).encode(
    x="Date:T",
    y="Price:Q",
    color="Type:N",
    tooltip=["Date", "Price", "Type"]
)

# --- CONFIDENCE BAND ---
if show_uncertainty and {"Lower", "Upper"}.issubset(pred_df.columns):

    band = alt.Chart(pred_filtered).mark_area(opacity=0.3).encode(
        x="Date:T",
        y="Lower:Q",
        y2="Upper:Q"
    )

    chart = band + line + points

else:
    chart = line + points

# --- FORECAST START LINE ---
if len(pred_df) > 0:
    split_line = alt.Chart(pd.DataFrame({
        "Date": [pred_df["Date"].min()]
    })).mark_rule(strokeDash=[5, 5]).encode(
        x="Date:T"
    )

    chart = chart + split_line

# --- DISPLAY ---
st.altair_chart(chart, use_container_width=True)

st.caption("Interactive view of historical and predicted gold prices with optional uncertainty bands.")