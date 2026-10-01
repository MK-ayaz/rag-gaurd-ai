"""Number and address formatting utilities."""

from __future__ import annotations


def shorten_address(address: str, chars: int = 6) -> str:
    """Shorten a 0x address to 0x1234…abcd format."""
    if not address or len(address) <= chars * 2 + 2:
        return address
    return f"{address[:chars]}…{address[-chars:]}"


def format_usd(amount: float) -> str:
    """Format a USD amount with appropriate suffixes (K, M, B)."""
    if amount is None:
        return "N/A"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.2f}K"
    return f"${amount:.2f}"


def format_percentage(value: float) -> str:
    """Format a percentage value."""
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


def format_token_name(name: str, symbol: str) -> str:
    """Combine token name and symbol for display."""
    if name and symbol:
        return f"{name} ({symbol})"
    return name or symbol or "Unknown Token"
