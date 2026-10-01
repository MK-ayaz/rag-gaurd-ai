"""Orchestrator Agent — runs all 4 analysis agents and computes the final risk score."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from models.risk_report import AgentResult, RiskReport
from agents.contract_auditor import ContractAuditorAgent
from agents.liquidity_agent import LiquidityAgent
from agents.holder_agent import HolderAgent
from agents.social_agent import SocialAgent
from agents.ai_explainer import generate_explanation, generate_static_explanation
from config import CHAINS

# Weights for each agent's contribution to the final score
WEIGHTS = {
    "contract": 0.35,
    "liquidity": 0.25,
    "holder": 0.25,
    "social": 0.15,
}


def _verdict_for_score(score: float) -> str:
    if score >= 80:
        return "SCAM - DO NOT BUY"
    elif score >= 60:
        return "HIGH RISK"
    elif score >= 40:
        return "CAUTION"
    elif score >= 20:
        return "LOW RISK"
    else:
        return "LIKELY SAFE"


def _verdict_emoji(verdict: str) -> str:
    prefix_map = {
        "SCAM": "🚨",
        "HIGH RISK": "⚠️",
        "CAUTION": "🟡",
        "LOW RISK": "🟢",
        "LIKELY SAFE": "✅",
    }
    for key, emoji in prefix_map.items():
        if verdict.startswith(key):
            return f"{emoji} {verdict}"
    return verdict


class RugGuardOrchestrator:
    def __init__(self, contract_address: str, chain: str):
        self.address = contract_address
        self.chain = chain
        self.agents = [
            ContractAuditorAgent(),
            LiquidityAgent(),
            HolderAgent(),
            SocialAgent(),
        ]

    def run_analysis(self, use_ai: bool = True) -> RiskReport:
        results: dict[str, AgentResult] = {}

        for agent in self.agents:
            try:
                results[agent.name] = agent.analyze(self.address, self.chain)
            except Exception as exc:
                results[agent.name] = AgentResult(
                    agent_name=agent.name,
                    risk_score=50,
                    checks={},
                    red_flags=[f"Agent error: {exc}"],
                    error=str(exc),
                )

        # Weighted final score
        final_score = 0.0
        total_weight = 0.0
        for name, weight in WEIGHTS.items():
            result = results.get(name)
            if result and not result.has_error():
                final_score += result.risk_score * weight
                total_weight += weight

        if total_weight > 0:
            final_score = final_score / total_weight if total_weight < 1.0 else final_score
        else:
            final_score = 50.0

        final_score = min(round(final_score), 100)

        # Extract token name/symbol from contract agent checks
        contract_checks = results.get("contract", None)
        token_name = "Unknown"
        token_symbol = "???"
        if contract_checks and not contract_checks.has_error():
            token_name = contract_checks.checks.get("token_name") or "Unknown"
            token_symbol = contract_checks.checks.get("token_symbol") or "???"

        verdict_text = _verdict_for_score(final_score)
        verdict = _verdict_emoji(verdict_text)

        report = RiskReport(
            contract_address=self.address,
            chain=self.chain,
            token_name=token_name,
            token_symbol=token_symbol,
            final_score=final_score,
            verdict=verdict,
            agent_results=results,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # AI explanation
        if use_ai:
            report.ai_explanation = generate_explanation(report)
            if not report.ai_explanation or report.ai_explanation.startswith("AI analysis unavailable"):
                report.ai_explanation = generate_static_explanation(report)
        else:
            report.ai_explanation = generate_static_explanation(report)

        return report
