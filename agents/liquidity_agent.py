"""Agent 2: Liquidity Agent — checks LP lock status, liquidity depth, and volume."""

from __future__ import annotations

from typing import Any, Dict, List

from models.risk_report import AgentResult
from services.goplus_service import get_token_security
from services.dexscreener_service import get_token_pairs, get_best_pair
from config import CHAINS


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip() == "1"
    return bool(value)


def _to_float(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def _parse_lock_time(raw: str) -> int:
    """Parse GoPlusLabs lock time string into days."""
    if not raw:
        return 0
    try:
        return int(float(raw)) // 86400
    except (ValueError, TypeError):
        return 0


def calculate_liquidity_risk(checks: Dict[str, Any]) -> int:
    risk = 0
    if not checks["lp_locked"]:
        risk += 40
    if checks["lp_lock_percentage"] < 50:
        risk += 20
    if checks["lp_lock_duration_days"] < 30:
        risk += 15
    if checks["total_liquidity_usd"] < 10000:
        risk += 15
    if checks["liquidity_to_mcap_ratio"] < 0.01:
        risk += 10
    return min(risk, 100)


class LiquidityAgent:
    name = "liquidity"
    display_name = "Liquidity Agent"
    description = "Checks LP lock status, liquidity depth, and trading volume"

    def analyze(self, address: str, chain: str) -> AgentResult:
        chain_cfg = CHAINS.get(chain, {})
        chain_id = chain_cfg.get("chain_id", 1)

        gp_data = get_token_security(chain_id, address)
        pairs = get_token_pairs(address)
        best_pair = get_best_pair(pairs)

        lp_holders = gp_data.get("lp_holders") or []

        # Determine LP lock info from GoPlusLabs lp_holders
        lp_locked = False
        lp_lock_percentage = 0.0
        lp_lock_duration_days = 0
        lp_lock_provider = ""

        for holder in lp_holders:
            if _to_bool(holder.get("is_locked")):
                lp_locked = True
                pct = _to_float(holder.get("percent")) * 100  # GoPlus gives 0-1 fraction
                lp_lock_percentage = max(lp_lock_percentage, pct)
                lp_lock_duration_days = max(
                    lp_lock_duration_days, _parse_lock_time(holder.get("lock_time", ""))
                )
                if holder.get("lock_tag"):
                    lp_lock_provider = holder["lock_tag"]

        total_liquidity_usd = 0.0
        volume_24h_usd = 0.0
        fdv = 0.0
        price_usd = 0.0

        if best_pair:
            liq = best_pair.get("liquidity") or {}
            vol = best_pair.get("volume") or {}
            total_liquidity_usd = _to_float(liq.get("usd"))
            volume_24h_usd = _to_float(vol.get("h24"))
            fdv = _to_float(best_pair.get("fdv"))
            price_usd = _to_float(best_pair.get("priceUsd"))

        # mcap approximation — use FDV if available
        mcap = fdv if fdv > 0 else 0.0
        liquidity_to_mcap_ratio = (
            total_liquidity_usd / mcap if mcap > 0 else 0.0
        )

        checks: Dict[str, Any] = {
            "lp_locked": lp_locked,
            "lp_lock_percentage": lp_lock_percentage,
            "lp_lock_duration_days": lp_lock_duration_days,
            "lp_lock_provider": lp_lock_provider,
            "total_liquidity_usd": total_liquidity_usd,
            "volume_24h_usd": volume_24h_usd,
            "liquidity_to_mcap_ratio": liquidity_to_mcap_ratio,
            "fdv": fdv,
            "price_usd": price_usd,
        }

        risk_score = calculate_liquidity_risk(checks)

        red_flags: List[str] = []
        if not lp_locked:
            red_flags.append("Liquidity is NOT locked — rug pull risk")
        if lp_lock_percentage < 50 and lp_locked:
            red_flags.append(f"Only {lp_lock_percentage:.1f}% of LP is locked")
        if lp_lock_duration_days < 30 and lp_locked:
            red_flags.append(f"LP locked for only {lp_lock_duration_days} days")
        if total_liquidity_usd < 10000:
            red_flags.append(f"Very low liquidity: ${total_liquidity_usd:,.0f}")
        if liquidity_to_mcap_ratio < 0.01 and mcap > 0:
            red_flags.append("Low liquidity-to-market-cap ratio")

        return AgentResult(
            agent_name=self.name,
            risk_score=risk_score,
            checks=checks,
            red_flags=red_flags,
        )
