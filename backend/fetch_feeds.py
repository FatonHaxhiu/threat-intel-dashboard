import os
import requests
import pandas as pd
from dotenv import load_dotenv
from io import StringIO

DATA_DIR = "data"

def fetch_alienvault(api_key):
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": api_key}
    r = requests.get(url, headers=headers)
    data = r.json()
    ips = []
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

def fetch_urlhaus():
    url = "https://urlhaus.abuse.ch/downloads/csv/"
    resp = requests.get(url)
    # URLhaus CSV has comment lines (starting with '#'); skip them
    lines = [line for line in resp.text.splitlines() if line and not line.startswith("#")]
    if not lines:
        print("No valid data lines found in URLhaus feed!")
        return
    csv_content = "\n".join(lines)
    df = pd.read_csv(StringIO(csv_content))
    # Extract IP from URL if present
    if "url" in df.columns:
        df["ip"] = df["url"].astype(str).str.extract(r"https?://(\d+\.\d+\.\d+\.\d+)")
    df["source"] = "URLhaus"
    save_cols = [col for col in ["url", "ip", "threat", "dateadded", "source"] if col in df.columns]
    out = df[save_cols]
    out.to_csv(os.path.join(DATA_DIR, "urlhaus_data.csv"), index=False)
    print(f"Saved {len(out)} URLhaus records.")

def main():
    load_dotenv()
    os.makedirs(DATA_DIR, exist_ok=True)
    av_key = os.getenv("ALIENVAULT_API_KEY")
    abuse_key = os.getenv("ABUSEIPDB_API_KEY")
    fetch_urlhaus()
    fetch_alienvault(av_key)
    fetch_abuseipdb(abuse_key)
    print("Fetched threat feeds.")

if __name__ == "__main__":
    main()