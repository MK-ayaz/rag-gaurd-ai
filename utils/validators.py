"""Address validation utilities."""

from __future__ import annotations

import re

_ADDRESS_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
_URL_PATH_PATTERN = re.compile(r"(?:/address/|/token/)(0x[a-fA-F0-9]{40})")


def normalize_address(raw: str) -> str:
    """Extract a bare EVM address from a URL, markdown link, or plain string."""
    if not raw:
        return ""
    s = raw.strip()
    # Strip surrounding markdown/URL syntax: [text](url), <url>, bare url
    url_match = re.search(r"https?://\S+", s)
    if url_match:
        s = url_match.group(0)
    path_match = _URL_PATH_PATTERN.search(s)
    if path_match:
        return path_match.group(1)
    # Remove leading/trailing junk that isn't hex
    s = re.sub(r"[^0xa-fA-F]", "", s)
    # Re-attach 0x prefix if present
    if s.startswith("0x"):
        return s
    return ""


def validate_address(address: str) -> bool:
    """Return True if address is a valid EVM-style address (0x + 40 hex)."""
    if not address:
        return False
    return bool(_ADDRESS_PATTERN.match(address.strip()))


def validate_chain(chain: str) -> bool:
    """Return True if the chain key is supported."""
    from config import CHAINS

    return chain in CHAINS
