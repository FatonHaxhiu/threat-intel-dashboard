import streamlit as st
import pandas as pd
import os
import altair as alt
import sys

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Run the backend fetcher if data files are missing
required_files = [
    "alienvault_ips.csv",
    "abuseipdb_ips.csv",
    "urlhaus_data.csv"
]
missing = [f for f in required_files if not os.path.exists(os.path.join(DATA_DIR, f))]
if missing:
    try:
        sys.path.append(os.path.abspath("./backend"))
        from fetch_feeds import main as fetch_main
        fetch_main()
    except Exception as e:
        st.error(f"Error running backend fetcher: {e}")

st.title("Threat Intel Dashboard")

# --- Load all threat CSVs into a single DataFrame ---
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

# --- Normalize column names for searching ---
all_data.columns = [c.lower() for c in all_data.columns]
if "ipaddress" in all_data.columns and "ip" not in all_data.columns:
    all_data = all_data.rename(columns={"ipaddress": "ip"})

# --- Visualization: Bar chart of IPs per source ---
st.subheader("📊 Number of Threat IPs by Source")
if "source" in all_data.columns and "ip" in all_data.columns:
    count_by_source = all_data.groupby("source")["ip"].count().reset_index()
    count_by_source = count_by_source.rename(columns={"ip": "count"})
    bar_chart = alt.Chart(count_by_source).mark_bar().encode(
        x=alt.X("source", sort="-y"),
        y="count",
        tooltip=["source", "count"]
    )
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.info("No 'source' or 'ip' column found in the data.")

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