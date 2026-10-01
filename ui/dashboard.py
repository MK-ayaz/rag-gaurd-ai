"""Main dashboard layout — modern professional UI."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from models.risk_report import RiskReport
from ui.styles import risk_class, risk_color_hex
from ui.risk_gauge import render_risk_gauge
from ui.agent_cards import render_agent_cards
from utils.formatters import shorten_address, format_usd, format_token_name


def render_header() -> None:
    """Render the app header with modern styling."""
    st.markdown(
        '<p class="main-title">🛡️ RugGuard AI</p>'
        '<p class="subtitle">Token Scam & Honeypot Detector — Powered by 4 AI Agents</p>'
        '<div class="accent-bar"></div>',
        unsafe_allow_html=True,
    )


def render_input_section(chain_options: dict, default_chain: str) -> tuple[str, str]:
    """Render the chain selector and address input. Returns (chain, address)."""
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    # Chain selector row
    st.markdown('<div class="input-label">🔗 Blockchain</div>', unsafe_allow_html=True)
    chain_labels = {k: v["name"] for k, v in chain_options.items()}
    selected_label = st.selectbox(
        "Blockchain",
        options=list(chain_labels.keys()),
        format_func=lambda k: chain_labels[k],
        index=list(chain_labels.keys()).index(default_chain) if default_chain in chain_labels else 0,
        label_visibility="collapsed",
    )
    chain_key = selected_label

    # Address input
    st.markdown('<div class="input-label" style="margin-top:16px;">📝 Token / Contract Address</div>', unsafe_allow_html=True)
    address = st.text_input(
        "Token / Contract Address",
        placeholder="0x... or Base58...",
        help="Paste the token contract address (not a wallet, profile, or transaction hash). EVM: 0x + 40 hex. Solana: 43-44 Base58 chars.",
        label_visibility="collapsed",
    )

    # Analyze button
    st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
    analyze_clicked = st.button("🔍 Analyze Token", type="primary", width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    return chain_key, (address.strip() if address else "")


def render_risk_score(report: RiskReport) -> None:
    """Render the main risk score gauge and verdict."""
    score = report.final_score
    css_class = risk_class(score)
    color = risk_color_hex(score)

    # Gauge chart
    gauge_fig: go.Figure = render_risk_gauge(score)
    st.plotly_chart(gauge_fig, width="stretch")

    # Verdict text
    st.markdown(
        f'<p class="risk-verdict {css_class}">{report.verdict}</p>',
        unsafe_allow_html=True,
    )

    # Token info
    token_display = format_token_name(report.token_name, report.token_symbol)
    chain_name = report.chain.title()
    st.markdown(
        f'<p class="token-info">'
        f"{token_display} · {chain_name} · {shorten_address(report.contract_address)}"
        f"</p>",
        unsafe_allow_html=True,
    )


def render_ai_explanation(report: RiskReport) -> None:
    """Render the AI-generated plain-language explanation."""
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header">🤖 AI Analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="ai-explanation">{report.ai_explanation}</div>',
        unsafe_allow_html=True,
    )


def render_detailed_findings(report: RiskReport) -> None:
    """Render expandable detailed findings for each agent."""
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header">📋 Detailed Findings</div>',
        unsafe_allow_html=True,
    )

    for agent_key, title, _subtitle, _accent in AGENT_META:
        result = report.agent_results.get(agent_key)
        if result is None:
            continue

        with st.expander(f"{title} — Score: {result.risk_score}/100", expanded=False):
            if result.has_error():
                st.error(f"Error during analysis: {result.error}")
            else:
                if result.red_flags:
                    st.markdown("**🚩 Red Flags:**")
                    for flag in result.red_flags:
                        st.markdown(f"- ⚠️ {flag}")
                    st.markdown("")

                st.markdown("**All Checks:**")
                checks = result.checks
                for name, val in checks.items():
                    if name in ("owner_address", "website_url", "twitter_url", "telegram_url"):
                        if val:
                            st.markdown(f"- 📝 **{name.replace('_', ' ').title()}**: `{val}`")
                        continue
                    _render_detail_item(name, val)


def _render_detail_item(name: str, value) -> None:
    display = name.replace("_", " ").title()
    if isinstance(value, bool):
        st.markdown(f"- **{display}**: {'Yes' if value else 'No'}")
    elif isinstance(value, float):
        if name.endswith("_percentage") or name.endswith("_ratio"):
            st.markdown(f"- **{display}**: {value:.2f}")
        elif "usd" in name or "liquidity" in name or "volume" in name:
            st.markdown(f"- **{display}**: {format_usd(value)}")
        else:
            st.markdown(f"- **{display}**: {value}")
    elif isinstance(value, int):
        st.markdown(f"- **{display}**: {value:,}")
    elif isinstance(value, str) and value:
        st.markdown(f"- **{display}**: {value}")
    else:
        st.markdown(f"- **{display}**: N/A")


def render_disclaimer() -> None:
    """Render the educational disclaimer."""
    st.markdown(
        '<div class="disclaimer">'
        "⚠️ <strong>RugGuard AI is for educational and informational purposes only.</strong><br>"
        "It does NOT constitute financial advice. Always do your own research (DYOR) "
        "before interacting with any token. The creators are not responsible for any "
        "financial losses."
        "</div>",
        unsafe_allow_html=True,
    )


def render_full_report(report: RiskReport) -> None:
    """Render the complete risk report dashboard."""
    render_risk_score(report)
    st.markdown("")
    render_agent_cards(report)
    st.markdown("")
    render_ai_explanation(report)
    st.markdown("")
    render_detailed_findings(report)
    st.markdown("")
    render_disclaimer()


# Re-export AGENT_META for agent_cards module
AGENT_META = [
    ("contract", "🔍 Contract Auditor", "Smart contract security", "#6366f1"),
    ("liquidity", "💧 Liquidity Agent", "LP lock & depth", "#06b6d4"),
    ("holder", "👥 Holder Agent", "Holder concentration", "#10b981"),
    ("social", "🌐 Social Agent", "Social presence", "#f59e0b"),
]
