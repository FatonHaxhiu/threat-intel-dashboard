from backend.fetch_feeds import fetch_alienvault

def test_fetch_alienvault_runs_without_crash(monkeypatch, tmp_path):
    import requests

    class DummyResponse:
        def json(self):
            return {"results": []}

    def dummy_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(requests, "get", dummy_get)

    # Patch DATA_DIR so test doesn't write to real files
    import backend.fetch_feeds
    backend.fetch_feeds.DATA_DIR = str(tmp_path)

    # Run function with a dummy api_key; should not crash
    fetch_alienvault("dummy_key")