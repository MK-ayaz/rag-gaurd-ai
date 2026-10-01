"""Honeypot.is API wrapper — honeypot detection fallback."""

from __future__ import annotations

import requests

from config import API_TIMEOUT

_BASE_URL = "https://api.honeypot.is/v2/IsHoneypot"


def check_honeypot(address: str, chain_id: int = 1) -> dict:
    """Check if a token is a honeypot via honeypot.is.

    Returns the parsed JSON response or {"error": ...} on failure.
    """
    params = {"address": address, "chainID": chain_id}
    try:
        resp = requests.get(_BASE_URL, params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}
