"""Main dashboard layout — modern branded experience."""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from models.risk_report import RiskReport
from ui.styles import risk_class, risk_color_hex
from ui.risk_gauge import render_risk_gauge
from utils.formatters import shorten_address, format_usd, format_token_name


AGENT_META = [
    ("contract", "📋", "Contract Auditor", "Smart contract security"),
    ("liquidity", "💧", "Liquidity Agent", "LP lock & depth"),
    ("holder", "👥", "Holder Agent", "Holder concentration"),
    ("social", "🌐", "Social Agent", "Social presence"),
]


def render_header() -> None:
    """Render the branded hero header."""
    st.markdown(
        '<div class="brand-container">'
        '<div class="brand-logo">🛡️</div>'
        '<div class="brand-name">RugGuard AI</div>'
        '<div class="brand-tagline">Token Scam & Honeypot Detector — Powered by 4 AI Agents</div>'
        '<div class="brand-divider"></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_input_section(chain_options: dict, default_chain: str) -> tuple[str, str]:
    """Render the branded search/input card."""
    chain_labels = {k: v["name"] for k, v in chain_options.items()}
    selected_label = chain_labels.get(default_chain, list(chain_labels.keys())[0])

    st.markdown('<div class="search-card">', unsafe_allow_html=True)

    col_chain, col_addr, col_btn = st.columns([1.2, 2.4, 0.8], gap="small")

    with col_chain:
        st.markdown('<span class="search-field-label">🔗 Chain</span>', unsafe_allow_html=True)
        chain_key = st.selectbox(
            "Blockchain",
            options=list(chain_labels.keys()),
            format_func=lambda k: chain_labels[k],
            index=list(chain_labels.keys()).index(default_chain) if default_chain in chain_labels else 0,
            label_visibility="collapsed",
        )

    with col_addr:
        st.markdown('<span class="search-field-label">📝 Contract Address</span>', unsafe_allow_html=True)
        address = st.text_input(
            "Token / Contract Address",
            placeholder="0x... or Base58...",
            help="Paste the token contract address (not a wallet, profile, or transaction hash). EVM: 0x + 40 hex. Solana: 43-44 Base58 chars.",
            label_visibility="collapsed",
        )

    with col_btn:
        st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
        analyze_clicked = st.button("🔍 Analyze", type="primary", width="stretch")

    st.markdown('</div>', unsafe_allow_html=True)

    return chain_key, (address.strip() if address else "")


def render_risk_score(report: RiskReport) -> None:
    """Render the main risk score gauge and verdict."""
    score = report.final_score
    css_class = risk_class(score)
    color = risk_color_hex(score)

    gauge_fig: go.Figure = render_risk_gauge(score)
    st.plotly_chart(gauge_fig, width="stretch", config={"displayModeBar": False})

    st.markdown(
        f'<div class="gauge-section" style="padding-top:0;">'
        f'<div class="risk-verdict {css_class}">{report.verdict}</div>'
        f'<div class="token-meta">'
        f'{format_token_name(report.token_name, report.token_symbol)}'
        f' · {report.chain.title()}'
        f' · {shorten_address(report.contract_address)}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_agent_cards_section(report: RiskReport) -> None:
    """Render the 4 agent cards in a responsive grid."""
    st.markdown(
        '<div class="section-title">📊 Agent Analysis</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    agent_colors = {
        "contract": "#6366f1",
        "liquidity": "#06b6d4",
        "holder": "#10b981",
        "social": "#f59e0b",
    }

    for idx, (agent_key, agent_emoji, title, subtitle) in enumerate(AGENT_META):
        result = report.agent_results.get(agent_key)
        with cols[idx]:
            if result is None:
                _render_empty_card(title, agent_emoji)
                continue

            color = agent_colors.get(agent_key, "#6366f1")

            if result.has_error():
                _render_error_card(title, subtitle, result.error, color, agent_emoji)
            else:
                _render_score_card(title, subtitle, result, color, agent_emoji)


def _render_empty_card(title: str, agent_emoji: str) -> None:
    st.markdown(
        f'<div class="agent-card" style="--agent-color: #475569;">'
        f'<div class="agent-card-header">'
        f'<div class="agent-icon" style="background: rgba(71,85,105,0.15); color: #64748b;">'
        f'{agent_emoji}'
        f'</div>'
        f'<div><div class="agent-title">{title}</div>'
        f'<div class="agent-subtitle">No data</div></div>'
        f'</div>'
        f'<div style="color:#334155; font-size:1.6rem; font-weight:700;">—</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_error_card(title: str, subtitle: str, error: str, color: str, agent_emoji: str) -> None:
    st.markdown(
        f'<div class="agent-card" style="--agent-color: #ef4444;">'
        f'<div class="agent-card-header">'
        f'<div class="agent-icon" style="background: rgba(239,68,68,0.1); color: #ef4444;">'
        f'{agent_emoji}'
        f'</div>'
        f'<div><div class="agent-title">{title}</div>'
        f'<div class="agent-subtitle">{subtitle}</div></div>'
        f'</div>'
        f'<div style="color:#475569; font-size:1.6rem; font-weight:700;">N/A</div>'
        f'<div class="agent-error">{error[:90]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_score_card(title: str, subtitle: str, result: AgentResult, color: str, agent_emoji: str) -> None:
    flags_html = ""
    for flag in result.red_flags[:2]:
        flags_html += f'<div class="agent-flag">{flag}</div>'

    st.markdown(
        f'<div class="agent-card" style="--agent-color: {color};">'
        f'<div class="agent-card-header">'
        f'<div class="agent-icon" style="background: {color}18; color: {color};">'
        f'{agent_emoji}'
        f'</div>'
        f'<div><div class="agent-title">{title}</div>'
        f'<div class="agent-subtitle">{subtitle}</div></div>'
        f'</div>'
        f'<div class="agent-score" style="color: {color};">{result.risk_score}</div>'
        f'<div class="agent-score-max">/ 100</div>'
        f'<div class="agent-bar-track">'
        f'<div class="agent-bar-fill" style="width: {result.risk_score}%; background: {color};"></div>'
        f'</div>'
        f'<div class="agent-flags">{flags_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    with st.expander("Details", expanded=False):
        _render_agent_details(result.checks)


def _render_agent_details(checks: dict) -> None:
    for name, val in checks.items():
        if name in ("owner_address", "website_url", "twitter_url", "telegram_url"):
            continue

        display = name.replace("_", " ").title()
        icon = "ℹ️"
        val_class = ""
        val_text = "N/A"

        if isinstance(val, bool):
            risky = _is_risky_check(name, val)
            icon = "❌" if risky else "✅"
            val_class = "danger" if risky else "safe"
            val_text = "Yes" if val else "No"
        elif isinstance(val, float):
            icon = "📊"
            val_text = f"{val:,.2f}"
            val_class = "danger" if val > 0 else ""
        elif isinstance(val, int) and not isinstance(val, bool):
            icon = "📊"
            val_text = f"{val:,}"
        elif isinstance(val, str) and val:
            icon = "📄"
            val_text = val

        st.markdown(
            f'<div class="check-row">'
            f'<span class="check-icon">{icon}</span>'
            f'<span class="check-label">{display}</span>'
            f'<span class="check-value {val_class}">{val_text}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _is_risky_check(name: str, value: bool) -> bool:
    risky_when_true = {
        "is_honeypot", "is_mintable", "can_take_back_ownership",
        "has_owner_change_balance", "has_hidden_owner", "is_proxy",
        "has_self_destruct", "has_blacklist_function",
        "has_trading_cooldown", "is_deployer_holding",
        "are_top_holders_contracts", "is_fake_token", "is_airdrop_scam",
    }
    risky_when_false = {
        "is_open_source", "lp_locked", "has_website",
        "has_twitter", "has_telegram", "is_on_coingecko",
    }
    if name in risky_when_true:
        return value
    if name in risky_when_false:
        return not value
    return False


def render_ai_explanation(report: RiskReport) -> None:
    """Render the AI-generated plain-language explanation."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">🤖 AI Analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="ai-box">{report.ai_explanation}</div>',
        unsafe_allow_html=True,
    )


def render_detailed_findings(report: RiskReport) -> None:
    """Render expandable detailed findings for each agent."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">📋 Detailed Findings</div>',
        unsafe_allow_html=True,
    )

    for agent_key, agent_emoji, title, _subtitle in AGENT_META:
        result = report.agent_results.get(agent_key)
        if result is None:
            continue

        with st.expander(f"{agent_emoji} {title} — Score: {result.risk_score}/100", expanded=False):
            if result.has_error():
                st.error(f"Error during analysis: {result.error}")
            else:
                if result.red_flags:
                    st.markdown("**Red Flags:**")
                    for flag in result.red_flags:
                        st.markdown(f"- ⚠️ {flag}")
                    st.markdown("")

                st.markdown("**All Checks:**")
                checks = result.checks
                for name, val in checks.items():
                    if name in ("owner_address", "website_url", "twitter_url", "telegram_url"):
                        if val:
                            st.markdown(f"- 📄 **{name.replace('_', ' ').title()}**: `{val}`")
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
        "⚠️ <strong>RugGuard AI is for educational and informational purposes only.</strong> "
        "It does NOT constitute financial advice. Always do your own research (DYOR) "
        "before interacting with any token. The creators are not responsible for any "
        "financial losses."
        "</div>",
        unsafe_allow_html=True,
    )


def render_full_report(report: RiskReport) -> None:
    """Render the complete risk report dashboard."""
    render_risk_score(report)
    render_agent_cards_section(report)
    render_ai_explanation(report)
    render_detailed_findings(report)
    render_disclaimer()
