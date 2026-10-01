"""Address validation utilities."""

from __future__ import annotations

import re

# EVM contract address: 0x + exactly 40 hex chars
_EVM_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
# Explorer URL path pattern — only /address/ and /token/ contain contract addresses
_URL_PATH_PATTERN = re.compile(r"(?:/address/|/token/)(0x[a-fA-F0-9]{40})")
# Transaction hash pattern (64 hex chars) — used to detect /tx/ URLs
_TX_HASH_PATTERN = re.compile(r"^0x[a-fA-F0-9]{64}$")


def is_tx_hash(address: str) -> bool:
    """Return True if the string looks like an EVM transaction hash (64 hex)."""
    if not address:
        return False
    return bool(_TX_HASH_PATTERN.match(address.strip()))


# Solana address: Base58, no 0x prefix, 43-44 chars
_SOL_PATTERN = re.compile(r"^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{43,44}$")


def normalize_address(raw: str) -> str:
    """Extract a bare address from a URL, markdown link, or plain string.

    Handles:
    - EVM explorer URLs: etherscan.io/address/..., /token/..., /tx/...
    - Solana explorer URLs: solscan.io/account/..., solscan.io/tx/...
    - Plain addresses (EVM or Solana)
    - Markdown-wrapped input
    """
    if not raw:
        return ""
    s = raw.strip()
    # Extract bare URL if input contains one
    url_match = re.search(r"https?://\S+", s)
    if url_match:
        s = url_match.group(0)
    # Try EVM explorer path extraction
    evm_path = _URL_PATH_PATTERN.search(s)
    if evm_path:
        return evm_path.group(1)
    # Try Solana explorer path: solscan.io/account/<base58_address>
    sol_path = re.search(r"solscan\.io/account/([123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{43,44})", s)
    if sol_path:
        return sol_path.group(1)
    # Plain input: detect Solana (Base58, no 0x) or EVM (starts with 0x)
    if re.match(r"^0x[a-fA-F0-9]+$", s):
        return s
    if _SOL_PATTERN.match(s):
        return s
    return ""


def validate_address(address: str) -> bool:
    """Return True if address is a valid EVM or Solana address."""
    if not address:
        return False
    a = address.strip()
    if _EVM_PATTERN.match(a):
        return True
    if _SOL_PATTERN.match(a):
        return True
    return False


def validate_chain(chain: str) -> bool:
    """Return True if the chain key is supported."""
    from config import CHAINS

    return chain in CHAINS
