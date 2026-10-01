"""GoPlusLabs API wrapper — token security data."""

from __future__ import annotations

import requests

from config import API_TIMEOUT

_BASE_URL = "https://api.gopluslabs.io/api/v1/token_security"


def get_token_security(chain_id: int, address: str) -> dict:
    """Fetch token security data from GoPlusLabs.

    Returns a dict of token security fields, or {"error": ...} on failure.
    The GoPlusLabs response nests the token data under result[address].
    """
    url = f"{_BASE_URL}/{chain_id}"
    params = {"contract_addresses": address}
    try:
        resp = requests.get(url, params=params, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        result_map = data.get("result") or {}
        # GoPlusLabs keys are lowercase addresses
        token_data = result_map.get(address.lower(), {})
        if not token_data:
            # Fallback: try the first key if there is exactly one
            if len(result_map) == 1:
                token_data = next(iter(result_map.values()))
        return token_data
    except Exception as exc:
        return {"error": str(exc)}
