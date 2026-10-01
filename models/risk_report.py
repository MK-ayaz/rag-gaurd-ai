"""Pydantic data models for RugGuard AI risk reports."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    agent_name: str
    risk_score: int = Field(ge=0, le=100)
    checks: Dict[str, Any] = Field(default_factory=dict)
    red_flags: List[str] = Field(default_factory=list)
    error: Optional[str] = None

    def has_error(self) -> bool:
        return self.error is not None


class RiskReport(BaseModel):
    contract_address: str
    chain: str
    token_name: str = "Unknown"
    token_symbol: str = "???"
    final_score: int = Field(ge=0, le=100)
    verdict: str = ""
    agent_results: Dict[str, AgentResult] = Field(default_factory=dict)
    ai_explanation: str = ""
    timestamp: str = ""

    def get_key_findings_text(self) -> str:
        lines: List[str] = []
        for name, result in self.agent_results.items():
            if result.has_error():
                lines.append(f"- {name}: Error during analysis ({result.error})")
                continue
            if result.red_flags:
                flags = "; ".join(result.red_flags[:5])
                lines.append(f"- {name} (score {result.risk_score}/100): {flags}")
            else:
                lines.append(f"- {name} (score {result.risk_score}/100): No major red flags")
        return "\n".join(lines)

    def get_agent_result(self, name: str) -> Optional[AgentResult]:
        return self.agent_results.get(name)
