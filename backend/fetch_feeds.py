import os
import requests
import pandas as pd
from dotenv import load_dotenv

DATA_DIR = "../data"

def fetch_alienvault(api_key):
    url = "https://otx.alienvault.com/api/v1/indicators/export"
    headers = {"X-OTX-API-KEY": api_key}
    params = {"type": "IPv4"}
    r = requests.get(url, headers=headers, params=params)
    # If it's plain text response (one IP per line)
    if r.headers.get("Content-Type", "").startswith("text"):
        lines = r.text.strip().split("\n")
        ips = [line for line in lines if line and not line.startswith("#")]
    else:
        # If JSON, filter for type == IPv4
        data = r.json()
        ips = [item["indicator"] for item in data if item.get("type") == "IPv4"]
    if ips:
        df = pd.DataFrame({"ip": ips, "source": "AlienVault"})
        df.to_csv(f"{DATA_DIR}/alienvault_ips.csv", index=False)
    else:
        print("No IPv4 indicators found from AlienVault.")

def fetch_abuseipdb(api_key):
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {"Key": api_key, "Accept": "application/json"}
    params = {"confidenceMinimum": 90}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()["data"]
    df = pd.DataFrame(data)
    if not df.empty:
        df["source"] = "AbuseIPDB"
        df.to_csv(f"{DATA_DIR}/abuseipdb_ips.csv", index=False)
    else:
        print("No IPs found from AbuseIPDB.")

def main():
    load_dotenv()
    os.makedirs(DATA_DIR, exist_ok=True)
    av_key = os.getenv("ALIENVAULT_API_KEY")
    abuse_key = os.getenv("ABUSEIPDB_API_KEY")
    fetch_alienvault(av_key)
    fetch_abuseipdb(abuse_key)
    print("Fetched threat feeds.")

if __name__ == "__main__":
    main()