"""Main dashboard layout — assembles all UI components into the full report view."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from models.risk_report import RiskReport
from ui.styles import risk_class, risk_color_hex, risk_class as _rc
from ui.risk_gauge import render_risk_gauge
from ui.agent_cards import render_agent_cards
from utils.formatters import shorten_address, format_usd, format_token_name


def render_header() -> None:
    """Render the app header."""
    st.markdown(
        '<p class="main-title">🛡️ RugGuard AI</p>'
        '<p class="subtitle">Token Scam & Honeypot Detector — '
        "Powered by 4 AI Agents</p>",
        unsafe_allow_html=True,
    )


def render_input_section(chain_options: dict, default_chain: str) -> tuple[str, str]:
    """Render the chain selector and address input. Returns (chain, address)."""
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    col_chain, col_addr = st.columns([1, 3])

    with col_chain:
        chain_labels = {k: v["name"] for k, v in chain_options.items()}
        selected_label = st.selectbox(
            "Blockchain",
            options=list(chain_labels.keys()),
            format_func=lambda k: chain_labels[k],
            index=list(chain_labels.keys()).index(default_chain) if default_chain in chain_labels else 0,
        )
        chain_key = selected_label

    with col_addr:
        address = st.text_input(
            "Token Contract Address",
            placeholder="0x...",
            help="Paste the token's smart contract address (0x followed by 40 hex characters)",
        )

    analyze_col, _ = st.columns([1, 3])
    with analyze_col:
        analyze_clicked = st.button("🔍 Analyze Token", type="primary", width="stretch")

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
        f'<p class="{css_class}">{report.verdict}</p>',
        unsafe_allow_html=True,
    )

    # Token info
    token_display = format_token_name(report.token_name, report.token_symbol)
    chain_name = report.chain.title()
    st.markdown(
        f'<p style="text-align:center; color:#a0a0b0; margin-top:-0.5rem;">'
        f"{token_display} · {chain_name} · {shorten_address(report.contract_address)}</p>",
        unsafe_allow_html=True,
    )


def render_ai_explanation(report: RiskReport) -> None:
    """Render the AI-generated plain-language explanation."""
    st.markdown("### 🤖 AI Analysis")
    st.markdown(
        f'<div class="ai-explanation">{report.ai_explanation}</div>',
        unsafe_allow_html=True,
    )


def render_detailed_findings(report: RiskReport) -> None:
    """Render expandable detailed findings for each agent."""
    st.markdown("### 📋 Detailed Findings")

    agent_labels = {
        "contract": "🔍 Contract Auditor",
        "liquidity": "💧 Liquidity Agent",
        "holder": "👥 Holder Agent",
        "social": "🌐 Social Agent",
    }

    for agent_key, label in agent_labels.items():
        result = report.agent_results.get(agent_key)
        if result is None:
            continue

        with st.expander(f"{label} — Score: {result.risk_score}/100", expanded=False):
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


def render_progress_updates() -> None:
    """Placeholder for showing agent progress updates during analysis."""
    pass


def render_full_report(report: RiskReport) -> None:
    """Render the complete risk report dashboard."""
    st.markdown("---")
    render_risk_score(report)
    st.markdown("")
    render_agent_cards(report)
    st.markdown("")
    render_ai_explanation(report)
    st.markdown("")
    render_detailed_findings(report)
    st.markdown("")
    render_disclaimer()
