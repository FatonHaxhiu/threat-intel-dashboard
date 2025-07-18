import streamlit as st
import pandas as pd
import glob
import os

DATA_DIR = "../data"

def load_data():
    all_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    dfs = []
    for file in all_files:
        df = pd.read_csv(file)
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame(columns=["ip", "source"])

st.title("Personal Threat Intelligence Dashboard")
st.markdown("Aggregating feeds from AlienVault OTX, AbuseIPDB, and more.")

df = load_data()
if df.empty:
    st.warning("No data available. Please run the backend fetcher.")
else:
    st.dataframe(df)
    st.subheader("Top 10 Malicious IPs")
    st.write(df["ip"].value_counts().head(10))
    st.subheader("Sources Distribution")
    st.bar_chart(df["source"].value_counts())