"""DexScreener API wrapper — liquidity & volume data."""

from __future__ import annotations

import requests

from config import API_TIMEOUT

_BASE_URL = "https://api.dexscreener.com/latest/dex/tokens"


def get_token_pairs(address: str) -> list:
    """Fetch DEX pair data for a token from DexScreener.

    Returns a list of pair dicts, or an empty list on failure.
    """
    url = f"{_BASE_URL}/{address}"
    try:
        resp = requests.get(url, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return data.get("pairs") or []
    except Exception:
        return []


def get_best_pair(pairs: list) -> dict:
    """Return the pair with the highest liquidity from a list of pairs."""
    if not pairs:
        return {}
    return max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0)
