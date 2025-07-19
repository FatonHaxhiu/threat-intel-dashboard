import streamlit as st
import pandas as pd
import os

DATA_DIR = "../data"

st.title("Threat Intel Dashboard")

# Load all threat CSVs into a single DataFrame
dfs = []
for fname in os.listdir(DATA_DIR):
    if fname.endswith(".csv"):
        try:
            df = pd.read_csv(os.path.join(DATA_DIR, fname))
            dfs.append(df)
        except Exception as e:
            st.warning(f"Could not load {fname}: {e}")
if dfs:
    all_data = pd.concat(dfs, ignore_index=True)
else:
    st.error("No threat data found. Please run the backend fetcher first.")
    st.stop()

# Normalize column names for searching
all_data.columns = [c.lower() for c in all_data.columns]
if "ipaddress" in all_data.columns and "ip" not in all_data.columns:
    all_data = all_data.rename(columns={"ipaddress": "ip"})

# --- IP Search Feature ---
st.header("🔎 IP Address Search")
ip_query = st.text_input("Enter an IP address to search:")

if ip_query:
    found = all_data[all_data["ip"].astype(str) == ip_query.strip()]
    if not found.empty:
        st.success(f"IP {ip_query} FOUND in threat feeds!")
        st.dataframe(found)
    else:
        st.info(f"IP {ip_query} not found in current threat lists.")

# --- Show the full table & allow download ---
st.header("All Threat IPs")
st.dataframe(all_data)

st.download_button(
    label="Download all threat IPs as CSV",
    data=all_data.to_csv(index=False),
    file_name="all_threat_ips.csv",
    mime="text/csv"
)