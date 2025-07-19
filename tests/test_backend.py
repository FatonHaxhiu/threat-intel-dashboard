from backend.fetch_feeds import fetch_alienvault, fetch_abuseipdb

def test_fetch_alienvault_runs_without_crash(monkeypatch, tmp_path):
    import requests

    # Mock response for AlienVault API
    class DummyResponse:
        def json(self):
            return {"results": [
                {"indicators": [
                    {"type": "IPv4", "indicator": "8.8.8.8"},
                    {"type": "domain", "indicator": "example.com"},
                    {"type": "IPv4", "indicator": "1.2.3.4"}
                ]}
            ]}

    def dummy_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", dummy_get)

    # Patch DATA_DIR to tmp_path
    import backend.fetch_feeds
    backend.fetch_feeds.DATA_DIR = str(tmp_path)

    # Run function with dummy key
    fetch_alienvault("dummy_key")

    # Check CSV created and content
    import pandas as pd
    csv_file = tmp_path / "alienvault_ips.csv"
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    assert "ip" in df.columns
    assert "source" in df.columns
    assert set(df["ip"]) == {"8.8.8.8", "1.2.3.4"}
    assert all(df["source"] == "AlienVault")


def test_fetch_abuseipdb_runs_without_crash(monkeypatch, tmp_path):
    import requests
    import pandas as pd

    # Mock response for AbuseIPDB API
    class DummyResponse:
        def json(self):
            return {"data": [
                {"ipAddress": "4.4.4.4", "abuseConfidenceScore": 100},
                {"ipAddress": "5.5.5.5", "abuseConfidenceScore": 95}
            ]}

    def dummy_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", dummy_get)

    # Patch DATA_DIR to tmp_path
    import backend.fetch_feeds
    backend.fetch_feeds.DATA_DIR = str(tmp_path)

    # Run function with dummy key
    fetch_abuseipdb("dummy_key")

    # Check CSV created and content
    csv_file = tmp_path / "abuseipdb_ips.csv"
    assert csv_file.exists()
    df = pd.read_csv(csv_file)
    assert "ipAddress" in df.columns or "ip" in df.columns
    assert "source" in df.columns
    assert set(df["ipAddress"] if "ipAddress" in df.columns else df["ip"]) == {"4.4.4.4", "5.5.5.5"}
    assert all(df["source"] == "AbuseIPDB")