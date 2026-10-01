"""Agent 3: Holder Agent — analyzes token holder distribution for concentration risk."""

from __future__ import annotations

from typing import Any, Dict, List

from models.risk_report import AgentResult
from services.goplus_service import get_token_security
from config import CHAINS


def _to_float(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def _to_int(value: Any) -> int:
    if value is None:
        return 0
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0


def calculate_holder_risk(checks: Dict[str, Any]) -> int:
    risk = 0
    if checks["top_holder_percentage"] > 40:
        risk += 35
    elif checks["top_holder_percentage"] > 20:
        risk += 20
    if checks["top_10_percentage"] > 80:
        risk += 25
    elif checks["top_10_percentage"] > 60:
        risk += 15
    if checks["is_deployer_holding"] and checks["deployer_percentage"] > 10:
        risk += 20
    if checks["total_holders"] < 100:
        risk += 15
    return min(risk, 100)


class HolderAgent:
    name = "holder"
    display_name = "Holder Agent"
    description = "Analyzes token holder distribution for concentration risk"

    def analyze(self, address: str, chain: str) -> AgentResult:
        chain_cfg = CHAINS.get(chain, {})
        chain_id = chain_cfg.get("chain_id", 1)

        gp_data = get_token_security(chain_id, address)

        holders = gp_data.get("holders") or []
        holder_count = _to_int(gp_data.get("holder_count")) or len(holders)

        # Calculate percentages — GoPlusLabs 'percent' is a 0-1 fraction
        top_holder_percentage = 0.0
        top_10_percentage = 0.0
        are_top_holders_contracts = False
        deployer_address = gp_data.get("creator_address", "") or ""
        is_deployer_holding = False
        deployer_percentage = 0.0

        # Herfindahl index for whale concentration
        herfindahl = 0.0

        for i, holder in enumerate(holders):
            pct = _to_float(holder.get("percent")) * 100  # convert to 0-100
            if i == 0:
                top_holder_percentage = pct
            if i < 10:
                top_10_percentage += pct

            addr = (holder.get("address") or "").lower()
            if addr and addr == deployer_address.lower():
                is_deployer_holding = True
                deployer_percentage = pct

            # Check if holder is a contract (has is_contract flag or address length check)
            if _to_int(holder.get("is_contract")) == 1 and i == 0:
                are_top_holders_contracts = True

            herfindahl += (pct / 100) ** 2

        checks: Dict[str, Any] = {
            "total_holders": holder_count,
            "top_holder_percentage": top_holder_percentage,
            "top_10_percentage": top_10_percentage,
            "is_deployer_holding": is_deployer_holding,
            "deployer_percentage": deployer_percentage,
            "are_top_holders_contracts": are_top_holders_contracts,
            "whale_concentration": herfindahl,
        }

        risk_score = calculate_holder_risk(checks)

        red_flags: List[str] = []
        if top_holder_percentage > 40:
            red_flags.append(f"Top holder controls {top_holder_percentage:.1f}% of supply")
        elif top_holder_percentage > 20:
            red_flags.append(f"Top holder owns {top_holder_percentage:.1f}% — elevated concentration")
        if top_10_percentage > 80:
            red_flags.append(f"Top 10 holders own {top_10_percentage:.1f}% — extreme concentration")
        elif top_10_percentage > 60:
            red_flags.append(f"Top 10 holders own {top_10_percentage:.1f}%")
        if is_deployer_holding and deployer_percentage > 10:
            red_flags.append(f"Deployer still holds {deployer_percentage:.1f}% of supply")
        if holder_count < 100:
            red_flags.append(f"Very few holders ({holder_count})")
        if are_top_holders_contracts:
            red_flags.append("Top holder is a contract — may have hidden control")

        return AgentResult(
            agent_name=self.name,
            risk_score=risk_score,
            checks=checks,
            red_flags=red_flags,
        )
