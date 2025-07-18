# Personal Threat Intelligence Dashboard

This project aggregates public threat intelligence feeds and visualizes them in a simple dashboard.

## Features
s
- Fetches IP reputation data from AlienVault OTX and AbuseIPDB
- Dockerized backend and frontend for easy setup
- Visualizes top malicious IPs and sources

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/<yourusername>/threat-intel-dashboard.git
   cd threat-intel-dashboard
   ```

2. **Set up API keys**

   Register for free accounts at:
   - [AlienVault OTX](https://otx.alienvault.com/)
   - [AbuseIPDB](https://www.abuseipdb.com/)

   Create a `.env` file in the project root:
   ```
   ALIENVAULT_API_KEY=your_alienvault_key_here
   ABUSEIPDB_API_KEY=your_abuseipdb_key_here
   ```

3. **Run the stack with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the dashboard**

   Navigate to [http://localhost:8501](http://localhost:8501) in your browser.

## Project Structure

```
backend/      # Fetches and processes threat feeds
frontend/     # Streamlit dashboard
data/         # Shared data volume (auto-created)
docker-compose.yml
.env          # API keys (not committed)
```

## License

MIT