"""Address validation utilities."""

from __future__ import annotations

import re

_ADDRESS_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")


def validate_address(address: str) -> bool:
    """Return True if address is a valid EVM-style address (0x + 40 hex)."""
    if not address:
        return False
    return bool(_ADDRESS_PATTERN.match(address.strip()))


def validate_chain(chain: str) -> bool:
    """Return True if the chain key is supported."""
    from config import CHAINS

    return chain in CHAINS
