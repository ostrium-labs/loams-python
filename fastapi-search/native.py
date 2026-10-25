"""A thin helper over the Loams native HTTP API (JSON).

These examples demonstrate the native HTTP JSON API alongside the SDK. The SDK
also provides app modules, builders, collection handles, SQL and streams.
"""
import json
import os
import urllib.error
import urllib.request

ENDPOINT = os.environ.get("LOAMS_ENDPOINT", "http://127.0.0.1:8080").rstrip("/")
API_KEY = os.environ.get("LOAMS_API_KEY", "")


def call(path: str, body: dict | None = None, method: str = "POST") -> dict:
    headers = {"content-type": "application/json"}
    if API_KEY:
        headers["authorization"] = f"Bearer {API_KEY}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(ENDPOINT + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"{method} {path}: HTTP {err.code}: {err.read().decode()[:300]}") from None
    return json.loads(raw) if raw else {}
