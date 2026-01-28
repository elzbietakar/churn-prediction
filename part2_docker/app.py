import os
import streamlit as st #type: ignore
import requests
import time

st.set_page_config(page_title="Churn Prediction", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #8989ff;
    }
    .stButton>button {
        background-color: #E78FAC;
        color: black;
    }
    .stTextInput>div>div>input {
        background-color: #E78FAC;
    }
    .stSelectbox>div>div>div {
        background-color: #E78FAC;
    }
    .stNumberInput>div>div>input {
        background-color: #E78FAC;
    }
    </style>
    """, unsafe_allow_html=True)

FEATURE_NAMES = ["gender", "SeniorCitizen", "Partner", "Dependents", "tenure", 
                 "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
                 "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", 
                 "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", 
                 "MonthlyCharges", "TotalCharges", "OptionalServices", "TenureQuantile", 
                 "MonthlyChargesQuantile"]

DEFAULT_CSV = "Female,0,No,No,7,Yes,No,Fiber optic,No,No,No,No,Yes,No,Month-to-month,Yes,Electronic check,79.7,6.375109995076221,1,Q1,Q3"

# Manage session-state keys for CSV and change tracking
if 'csv_field' not in st.session_state:
    st.session_state.csv_field = DEFAULT_CSV
if 'last_csv' not in st.session_state:
    st.session_state.last_csv = st.session_state.csv_field
if 'last_features' not in st.session_state:
    st.session_state.last_features = ''
if 'sync_from_sidebar' not in st.session_state:
    st.session_state.sync_from_sidebar = ''

# If we have a pending sync request from the sidebar, update csv_field before widget instantiation
if st.session_state.sync_from_sidebar:
    st.session_state.csv_field = st.session_state.sync_from_sidebar
    st.session_state.last_csv = st.session_state.sync_from_sidebar
    st.session_state.sync_from_sidebar = ''

# Main app title and CSV input
st.title("Churn Prediction")
csv_input = st.text_input("CSV Input:", key="csv_field")

# Helper: parse a CSV string into dict
def parse_csv_to_dict(csv_str):
    vals = csv_str.split(',')
    if len(vals) != len(FEATURE_NAMES):
        return None
    return {FEATURE_NAMES[i]: vals[i].strip() for i in range(len(FEATURE_NAMES))}

# If the CSV widget changed since last run, push values into sidebar session state
parsed = parse_csv_to_dict(st.session_state.csv_field)
if st.session_state.csv_field != st.session_state.last_csv and parsed:
    for name in FEATURE_NAMES:
        key = f"input_{name}"
        val = parsed.get(name, "")
        if name in ["tenure", "OptionalServices"]:
            try:
                st.session_state[key] = int(val) if val != "" else 0
            except Exception:
                st.session_state[key] = 0
        elif name in ["MonthlyCharges", "TotalCharges"]:
            try:
                st.session_state[key] = float(val) if val != "" else 0.0
            except Exception:
                st.session_state[key] = 0.0
        else:
            st.session_state[key] = val
    st.session_state.last_csv = st.session_state.csv_field
    # remember features string to avoid immediate flip
    st.session_state.last_features = ','.join([str(st.session_state.get(f"input_{n}", '')) for n in FEATURE_NAMES])
# Sidebar for manual input (widgets read/write from session state keys)
st.sidebar.header("Feature Input")
features = {}

# callback to queue CSV sync when any sidebar widget changes
def queue_sync():
    csv_from_features = ','.join([str(st.session_state.get(f"input_{n}", '')) for n in FEATURE_NAMES])
    st.session_state.sync_from_sidebar = csv_from_features
    st.session_state.last_features = csv_from_features
for name in FEATURE_NAMES:
    key = f"input_{name}"
    # ensure a default exists in session state
    if key not in st.session_state:
        default = parsed.get(name, "") if parsed else ""
        st.session_state[key] = int(default) if name in ["tenure", "OptionalServices"] and default != "" else (
            float(default) if name in ["MonthlyCharges", "TotalCharges"] and default != "" else default)
    if name in ["tenure", "OptionalServices"]:
        # ensure the widget uses an int default and returns ints
        try:
            int_default = int(st.session_state.get(key, 0) if st.session_state.get(key, 0) != '' else 0)
        except Exception:
            int_default = 0
        features[name] = st.sidebar.number_input(
            name,
            key=key,
            value=int_default,
            step=1,
            format="%d",
            on_change=queue_sync,
        )
    elif name in ["MonthlyCharges", "TotalCharges"]:
        features[name] = st.sidebar.number_input(name, key=key, on_change=queue_sync)
    else:
        features[name] = st.sidebar.text_input(name, key=key, on_change=queue_sync)

# Predict button and result
col1, col2 = st.columns([1, 3])
with col1:
    predict_btn = st.button("Predict", use_container_width=True)

API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000")

if predict_btn:
    response = requests.post(f"{API_URL}/api/predict", json=features)
    result = response.json()
    st.success(f"Prediction: {result['predictions'][0]} (Probability: {result['probabilities'][0]:.4f})")

# Server statistics at bottom right
st.markdown("---")
col_left, col_right = st.columns([3, 1])
with col_right:
    # persistent visibility flag for the metrics panel
    if 'metrics_visible' not in st.session_state:
        st.session_state.metrics_visible = False

    def _toggle_metrics():
        st.session_state.metrics_visible = not st.session_state.metrics_visible

    btn_label = "Hide server statistics" if st.session_state.metrics_visible else "Show server statistics"
    # use on_click callback so the state flips before the rerun and the label stays in-sync
    st.button(btn_label, key="metrics_toggle", on_click=_toggle_metrics)

    if st.session_state.metrics_visible:
        metrics_placeholder = col_right.empty()
        for _ in range(10000):
            # respect a user toggle-off during the update loop
            if not st.session_state.metrics_visible:
                break
            try:
                response = requests.get(f"{API_URL}/metrics")
                metrics = response.json()
                metrics_placeholder.json(metrics)
            except Exception as e:
                metrics_placeholder.error(f"Error fetching metrics: {e}")
                break
            time.sleep(1)