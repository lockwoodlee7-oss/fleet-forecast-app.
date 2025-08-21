# fleet_forecast_app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fleet Workload Forecast", layout="wide")

st.title("🚆 Fleet Workload vs Resource Forecasting Tool")
st.markdown("Designed for Northern Trains Limited")

# --- Depot Selection ---
depots = ["Allerton", "Heaton", "Neville Hill", "Newton Heath", "Hull BG", "Shipley"]
selected_depot = st.sidebar.selectbox("Select Depot", depots)

# --- Resource Inputs ---
st.sidebar.header("Resource Assumptions")
headcount = st.sidebar.number_input("Total Headcount", min_value=0, value=50)
shift_length = st.sidebar.number_input("Shift Length (hrs)", min_value=1, value=8)
shifts_per_week = st.sidebar.number_input("Shifts per Week", min_value=1, value=5)
people_per_shift = st.sidebar.number_input("People per Shift", min_value=1, value=10)

leave_pct = st.sidebar.slider("Annual Leave %", 0.0, 1.0, 0.1)
sickness_pct = st.sidebar.slider("Sickness %", 0.0, 1.0, 0.05)
training_pct = st.sidebar.slider("Training %", 0.0, 1.0, 0.05)
efficiency_pct = st.sidebar.slider("Efficiency %", 0.0, 1.0, 0.85)

# --- Calculations ---
raw_hours = headcount * shift_length * shifts_per_week
adjusted_hours = raw_hours * (1 - leave_pct - sickness_pct - training_pct) * efficiency_pct

# --- Placeholder Workload Data ---
required_hours = {
    "Allerton": 1200,
    "Heaton": 950,
    "Neville Hill": 1600,
    "Newton Heath": 1100,
    "Hull BG": 700,
    "Shipley": 500
}

required = required_hours.get(selected_depot, 0)
surplus = adjusted_hours - required

# --- Output ---
st.subheader(f"Depot: {selected_depot}")
st.metric("Available Hours/Week", f"{adjusted_hours:.1f}")
st.metric("Required Hours/Week", f"{required:.1f}")
st.metric("Surplus/Deficit", f"{surplus:.1f}", delta=f"{surplus:.1f}")

# --- Scenario Table ---
st.subheader("Scenario Summary")
summary_df = pd.DataFrame({
    "Depot": [selected