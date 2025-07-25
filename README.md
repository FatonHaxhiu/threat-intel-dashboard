# Threat Intel Dashboard

[![CI](https://github.com/FatonHaxhiu/threat-intel-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/FatonHaxhiu/threat-intel-dashboard/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Pandas](https://img.shields.io/badge/pandas-2.2.2-darkgreen?logo=pandas)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.34.0-red?logo=streamlit)](https://streamlit.io/)
[![Requests](https://img.shields.io/badge/requests-2.31.0-blue?logo=python)](https://requests.readthedocs.io/)
[![python-dotenv](https://img.shields.io/badge/dotenv-1.0.1-lightgrey?logo=python)](https://pypi.org/project/python-dotenv/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Last Update](https://img.shields.io/badge/last%20update-July%202025-blue)

---

## 🚀 Purpose of the Project

The Threat Intel Dashboard is an open-source tool to help security analysts and IT teams easily aggregate, visualize, and search threat intelligence data from multiple sources. By collecting indicators of compromise (IOCs) such as suspicious IP addresses from feeds like AlienVault OTX and AbuseIPDB, the dashboard enables rapid situational awareness, threat hunting, and actionable security response.

**Key Features:**
- Fetches and aggregates threat IP addresses from multiple feeds
- Presents summary stats, visualizations, and a searchable interface
- Allows lookup of specific IPs to check if they appear in threat feeds
- Supports exporting of current threat lists for further use (e.g., in firewalls)
- Built for extensibility—add new feeds or enrichments easily!
- **Continuous Integration:** Automated testing with GitHub Actions and pytest for code reliability

---

## ⚡️ How to Use

### 1. **Clone the Repository**

```bash
git clone https://github.com/FatonHaxhiu/threat-intel-dashboard.git
cd threat-intel-dashboard
```

### 2. **Set Up API Keys**

Create a `.env` file in the root directory with your API keys:

```
ALIENVAULT_API_KEY=your_otx_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_key_here
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Fetch Threat Feed Data**

Run the backend fetcher script to download and process the latest data:

```bash
python3 backend/fetch_feeds.py
```

You should see output about how many IPs were saved from each feed. If you hit a rate limit, wait until your quota resets.

### 5. **Run the Dashboard**

Start the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

This will open your default browser to the dashboard interface (usually at `http://localhost:8501`).

### 6. **Testing and CI**

- **Run all tests locally:**  
  ```bash
  pytest
  ```
- **CI with GitHub Actions:**  
  Every commit and pull request triggers automated tests (see badge above).  
  Tests are located in the `tests/` directory and use `pytest` with mocking to avoid external API calls.

### 7. **Explore and Search**

- **Search for specific IPs:** Use the search box to check if an IP is present in the threat feeds.
- View summary stats and visualizations on the main page
- Use the search box to look up specific IPs
- Browse the full table of threat IPs
- Download the combined IP list as CSV

---
## 🧩 Extending the Project

- Add new threat feeds by creating new functions in `backend/fetch_feeds.py`
- Add enrichments (ASN, geo, etc.) using APIs like ipinfo.io or ip-api.com
- Improve frontend visualizations or add new search/filter features
- Write more tests for new features and keep CI green!

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).