"""AI Explainer Agent — uses Groq (Llama 3) for plain-language risk summaries."""

from __future__ import annotations

from models.risk_report import RiskReport
from services.groq_service import generate_summary


def generate_explanation(risk_report: RiskReport) -> str:
    """Generate a plain-language explanation of the risk report via Groq."""
    prompt = f"""You are a crypto security analyst. Explain this token analysis in simple language for a beginner. Be direct and clear.

Token: {risk_report.token_name} ({risk_report.token_symbol})
Chain: {risk_report.chain}
Contract: {risk_report.contract_address}
Final Risk Score: {risk_report.final_score}/100
Verdict: {risk_report.verdict}

Contract Risk: {risk_report.agent_results.get('contract', None) and risk_report.agent_results['contract'].risk_score}/100
Liquidity Risk: {risk_report.agent_results.get('liquidity', None) and risk_report.agent_results['liquidity'].risk_score}/100
Holder Risk: {risk_report.agent_results.get('holder', None) and risk_report.agent_results['holder'].risk_score}/100
Social Risk: {risk_report.agent_results.get('social', None) and risk_report.agent_results['social'].risk_score}/100

Key findings:
{risk_report.get_key_findings_text()}

Write a 3-4 sentence explanation in simple English. Do NOT give financial advice. Only explain the risk factors found."""

    return generate_summary(prompt)


def generate_static_explanation(risk_report: RiskReport) -> str:
    """Generate a rule-based explanation as fallback when Groq is unavailable."""
    score = risk_report.final_score
    findings = risk_report.get_key_findings_text()

    if score >= 80:
        intro = "This token shows severe red flags and should be treated as high-risk."
    elif score >= 60:
        intro = "This token has multiple significant risk factors."
    elif score >= 40:
        intro = "This token has some cautionary signals worth investigating."
    elif score >= 20:
        intro = "This token appears relatively low-risk but is not guaranteed safe."
    else:
        intro = "This token appears likely safe based on available data."

    return f"{intro} {findings}"
