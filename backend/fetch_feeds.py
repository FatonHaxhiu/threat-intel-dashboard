import os
import requests
import pandas as pd
from dotenv import load_dotenv

DATA_DIR = "../data"

def fetch_alienvault(api_key):
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": api_key}
    r = requests.get(url, headers=headers)
    data = r.json()
    ips = []
    # Each pulse in results has an 'indicators' array; each indicator has 'type' and 'indicator'
    for pulse in data.get("results", []):
        for indicator in pulse.get("indicators", []):
            if indicator.get("type") == "IPv4":
                ips.append(indicator.get("indicator"))
    if ips:
        df = pd.DataFrame({"ip": ips, "source": "AlienVault"})
        df.to_csv(f"{DATA_DIR}/alienvault_ips.csv", index=False)
        print(f"Saved {len(ips)} AlienVault IPs from DirectConnect API.")
    else:
        print("No IPv4 indicators found from AlienVault.")

def fetch_abuseipdb(api_key):
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {"Key": api_key, "Accept": "application/json"}
    params = {"confidenceMinimum": 90}
    r = requests.get(url, headers=headers, params=params)
    try:
        resp = r.json()
        if "data" not in resp:
            print("AbuseIPDB response did not contain 'data' key. Full response:")
            print(resp)
            return
        data = resp["data"]
        df = pd.DataFrame(data)
        if not df.empty:
            df["source"] = "AbuseIPDB"
            df.to_csv(f"{DATA_DIR}/abuseipdb_ips.csv", index=False)
            print(f"Saved {len(df)} AbuseIPDB IPs.")
        else:
            print("No IPs found from AbuseIPDB.")
    except Exception as e:
        print(f"Error parsing AbuseIPDB response: {e}")
        print("Raw response text:")
        print(r.text)

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