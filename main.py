# app/main.py
import time
import streamlit as st
import pandas as pd
from stock_data import batch_fetch

st.set_page_config(page_title="Live Stock Monitor", layout="wide")
st.title("🔄 Live Stock Monitor")

# ----------------------------------------------------
# 1. Get user input
# ----------------------------------------------------
tickers = st.text_input(
    "Tickers (comma separated)",
    value="AAPL,MSFT,TSLA"
).split(",")
tickers = [t.strip().upper() for t in tickers if t.strip()]
if not tickers:
    st.warning("Enter at least one ticker.")
    st.stop()

# ----------------------------------------------------
# 2. How often to refresh
# ----------------------------------------------------
refresh = st.slider("Refresh every", 5, 60, 15, step=5)

# ----------------------------------------------------
# 3. Store last fetch time in session_state
# ----------------------------------------------------
if "last_fetch" not in st.session_state:
    st.session_state.last_fetch = 0
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# ----------------------------------------------------
# 4. Fetch new data only if the interval has passed
# ----------------------------------------------------
if time.time() - st.session_state.last_fetch > refresh:
    st.session_state.last_fetch = time.time()
    try:
        st.info("Fetching data…")
        st.session_state.df = batch_fetch(tickers)          # this may take a few seconds
        st.success("Data ready!")
    except Exception as exc:
        st.error(f"❌ Could not fetch data: {exc}")

# ----------------------------------------------------
# 5. Render the table / chart
# ----------------------------------------------------
if not st.session_state.df.empty:
    st.dataframe(st.session_state.df, hide_index=True)
    if {"timestamp", "price"}.issubset(st.session_state.df.columns):
        st.line_chart(
            st.session_state.df.set_index("timestamp")[["price"]].astype(float)
        )

# ----------------------------------------------------
# 6. Add a manual refresh button
# ----------------------------------------------------
if st.button("Refresh now"):
    st.session_state.last_fetch = 0          # force a refresh on next render
