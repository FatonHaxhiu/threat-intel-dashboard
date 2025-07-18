import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_DIR = "../data"

def load_feed(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df, os.path.getmtime(path)
    else:
        return pd.DataFrame(columns=['ip', 'source']), None

def format_time(epoch):
    if epoch is None:
        return "Never"
    dt = datetime.fromtimestamp(epoch)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Load data
av_df, av_time = load_feed("alienvault_ips.csv")
abuse_df, abuse_time = load_feed("abuseipdb_ips.csv")

# Merge feeds for search
all_df = pd.concat([av_df, abuse_df], ignore_index=True).drop_duplicates(subset=["ip", "source"])
unique_ips = all_df["ip"].nunique()
sources = all_df["source"].unique()

st.title("Threat Intel Dashboard")

# Feed freshness
st.sidebar.header("Feed Status")
st.sidebar.write(f"**AlienVault OTX:** {len(av_df)} IPs (updated {format_time(av_time)})")
st.sidebar.write(f"**AbuseIPDB:** {len(abuse_df)} IPs (updated {format_time(abuse_time)})")
st.sidebar.write(f"**Total Unique IPs:** {unique_ips}")

# Summary stats
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("AlienVault IPs", len(av_df))
col2.metric("AbuseIPDB IPs", len(abuse_df))
col3.metric("Total Unique IPs", unique_ips)

# Bar chart of source counts
source_counts = all_df.groupby("source")["ip"].nunique()
st.bar_chart(source_counts)

# IP search
st.subheader("IP Lookup")
ip_query = st.text_input("Search for an IP address")
if ip_query:
    hits = all_df[all_df["ip"] == ip_query]
    if not hits.empty:
        st.success(f"Found {ip_query} in: {', '.join(hits['source'].unique())}")
        st.table(hits)
    else:
        st.warning(f"{ip_query} not found in current threat feeds.")

# Show all data
st.subheader("All Threat IPs")
st.dataframe(all_df.sort_values("ip"), use_container_width=True)

# Download button
st.download_button(
    label="Download All IPs (CSV)",
    data=all_df.to_csv(index=False),
    file_name="all_threat_ips.csv",
    mime="text/csv"
)