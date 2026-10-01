"""Agent 1: Contract Auditor — analyzes smart contract code for malicious patterns."""

from __future__ import annotations

from typing import Any, Dict, List

from models.risk_report import AgentResult
from services.goplus_service import get_token_security
from services.honeypot_service import check_honeypot
from config import CHAINS


def _to_bool(value: Any) -> bool:
    """GoPlusLabs returns string '1'/'0'; convert to bool."""
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


def calculate_contract_risk(checks: Dict[str, Any]) -> int:
    risk = 0
    if checks["is_honeypot"]:
        risk += 40
    if checks["is_mintable"]:
        risk += 15
    if checks["can_take_back_ownership"]:
        risk += 15
    if checks["has_owner_change_balance"]:
        risk += 10
    if checks["has_hidden_owner"]:
        risk += 5
    if checks["has_blacklist_function"]:
        risk += 5
    if checks["sell_tax"] > 10:
        risk += 5
    if checks["buy_tax"] > 10:
        risk += 5
    if not checks["is_open_source"]:
        risk += 10
    return min(risk, 100)


class ContractAuditorAgent:
    name = "contract"
    display_name = "Contract Auditor"
    description = "Analyzes smart contract code for malicious patterns"

    def analyze(self, address: str, chain: str) -> AgentResult:
        chain_cfg = CHAINS.get(chain, {})
        chain_id = chain_cfg.get("chain_id", 1)

        gp_data = get_token_security(chain_id, address)

        if "error" in gp_data:
            # Fallback to honeypot.is
            hp = check_honeypot(address, chain_id)
            if "error" in hp:
                return AgentResult(
                    agent_name=self.name,
                    risk_score=50,
                    checks={},
                    red_flags=["Data unavailable from all contract data sources"],
                    error=gp_data["error"],
                )
            is_honeypot = hp.get("honeypot", False)
            checks: Dict[str, Any] = {
                "is_honeypot": is_honeypot,
                "is_mintable": False,
                "can_take_back_ownership": False,
                "has_owner_change_balance": False,
                "has_hidden_owner": False,
                "is_proxy": False,
                "has_self_destruct": False,
                "is_open_source": False,
                "has_blacklist_function": False,
                "has_trading_cooldown": False,
                "sell_tax": 0.0,
                "buy_tax": 0.0,
            }
        else:
            checks = {
                "is_honeypot": _to_bool(gp_data.get("is_honeypot")),
                "is_mintable": _to_bool(gp_data.get("is_mintable")),
                "can_take_back_ownership": _to_bool(gp_data.get("can_take_back_ownership")),
                "has_owner_change_balance": _to_bool(gp_data.get("owner_change_balance")),
                "has_hidden_owner": _to_bool(gp_data.get("hidden_owner")),
                "is_proxy": _to_bool(gp_data.get("is_proxy")),
                "has_self_destruct": _to_bool(gp_data.get("selfdestruct")),
                "is_open_source": _to_bool(gp_data.get("is_open_source")),
                "has_blacklist_function": _to_bool(gp_data.get("is_blacklisted")),
                "has_trading_cooldown": _to_bool(gp_data.get("trading_cooldown")),
                "sell_tax": _to_float(gp_data.get("sell_tax")),
                "buy_tax": _to_float(gp_data.get("buy_tax")),
                "owner_address": gp_data.get("owner_address", ""),
                "token_name": gp_data.get("token_name", ""),
                "token_symbol": gp_data.get("token_symbol", ""),
            }

        risk_score = calculate_contract_risk(checks)

        red_flags: List[str] = []
        if checks["is_honeypot"]:
            red_flags.append("Honeypot detected: you may not be able to sell")
        if checks["is_mintable"]:
            red_flags.append("Owner can mint infinite new tokens")
        if checks["can_take_back_ownership"]:
            red_flags.append("Owner can reclaim ownership after renouncing")
        if checks["has_owner_change_balance"]:
            red_flags.append("Owner can modify user balances directly")
        if checks["has_hidden_owner"]:
            red_flags.append("Hidden owner detected")
        if checks["has_blacklist_function"]:
            red_flags.append("Blacklist function present — owner can block wallets")
        if checks["sell_tax"] > 10:
            red_flags.append(f"High sell tax: {checks['sell_tax']:.1f}%")
        if checks["buy_tax"] > 10:
            red_flags.append(f"High buy tax: {checks['buy_tax']:.1f}%")
        if not checks["is_open_source"]:
            red_flags.append("Source code not verified")

        return AgentResult(
            agent_name=self.name,
            risk_score=risk_score,
            checks=checks,
            red_flags=red_flags,
        )
