"""Etherscan / BscScan / PolygonScan API wrapper — contract source & token info."""

from __future__ import annotations

import requests

from config import API_TIMEOUT, CHAINS


def get_source_code(address: str, chain: str) -> dict:
    """Fetch verified source code for a contract from the chain explorer.

    Returns a dict with source code info, or {"error": ...} on failure.
    """
    chain_cfg = CHAINS.get(chain)
    if not chain_cfg:
        return {"error": f"Unsupported chain: {chain}"}

    import os

    api_key = os.getenv(chain_cfg["api_key_env"], "")
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key,
    }
    try:
        resp = requests.get(chain_cfg["explorer_api"], params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "1" and data.get("result"):
            return data["result"][0]
        return {"error": data.get("message", "No source code found")}
    except Exception as exc:
        return {"error": str(exc)}


def get_token_info(address: str, chain: str) -> dict:
    """Fetch token metadata (name, symbol, decimals, total supply) from explorer."""
    chain_cfg = CHAINS.get(chain)
    if not chain_cfg:
        return {"error": f"Unsupported chain: {chain}"}

    import os

    api_key = os.getenv(chain_cfg["api_key_env"], "")
    params = {
        "module": "token",
        "action": "tokeninfo",
        "contractaddress": address,
        "apikey": api_key,
    }
    try:
        resp = requests.get(chain_cfg["explorer_api"], params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "1" and data.get("result"):
            return data["result"][0]
        return {}
    except Exception:
        return {}
