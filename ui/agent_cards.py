"""Agent result cards — one per analysis agent."""

from __future__ import annotations

import streamlit as st

from models.risk_report import AgentResult, RiskReport
from ui.styles import risk_class, risk_color_hex

# Display order and metadata for each agent
AGENT_META = [
    ("contract", "🔍 Contract Auditor", "Checks for honeypot, minting, blacklist, hidden owner"),
    ("liquidity", "💧 Liquidity Agent", "Checks LP lock, liquidity depth, volume"),
    ("holder", "👥 Holder Agent", "Checks holder concentration, deployer holdings"),
    ("social", "🌐 Social Agent", "Checks social links, token age, scam reports"),
]


def _render_score_dots(score: int) -> str:
    """Render 3 dots representing risk level for an agent card."""
    if score >= 70:
        return "🔴🔴🔴"
    elif score >= 50:
        return "🔴🔴🟡"
    elif score >= 30:
        return "🟡🟡🟢"
    else:
        return "🟢🟢🟢"


def render_agent_cards(report: RiskReport) -> None:
    """Render the 4 agent result cards in a row."""
    cols = st.columns(4)

    for idx, (agent_key, title, subtitle) in enumerate(AGENT_META):
        result: AgentResult | None = report.agent_results.get(agent_key)
        with cols[idx]:
            if result is None:
                st.markdown(f"**{title}**\n\n_No data_")
                continue

            color = risk_color_hex(result.risk_score)
            dots = _render_score_dots(result.risk_score)

            if result.has_error():
                st.markdown(
                    f"""<div class="agent-card">
                    <div class="agent-card-title">{title}</div>
                    <div class="agent-card-score" style="color: #888;">N/A</div>
                    <div style="font-size: 1.2rem;">⚪⚪⚪</div>
                    <div style="font-size: 0.8rem; color: #ff6b6b; margin-top: 0.5rem;">Error: {result.error[:60]}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                flags_html = ""
                for flag in result.red_flags[:3]:
                    flags_html += f'<div class="agent-flag">⚠ {flag}</div>'

                st.markdown(
                    f"""<div class="agent-card">
                    <div class="agent-card-title">{title}</div>
                    <div class="agent-card-score" style="color: {color};">{result.risk_score}<span style="font-size:1rem;">/100</span></div>
                    <div style="font-size: 1.4rem; margin-bottom: 0.5rem;">{dots}</div>
                    {flags_html}
                    </div>""",
                    unsafe_allow_html=True,
                )

                # Expandable details
                with st.expander("Details", expanded=False):
                    for check_name, check_val in result.checks.items():
                        if check_name in ("owner_address", "website_url", "twitter_url", "telegram_url"):
                            continue
                        _render_check_row(check_name, check_val)


def _render_check_row(name: str, value) -> None:
    """Render a single check as a checkmark or X row."""
    display_name = name.replace("_", " ").title()

    if isinstance(value, bool):
        icon = "✅" if not _is_risky_check(name, value) else "❌"
        st.markdown(f"{icon} **{display_name}**: {'Yes' if value else 'No'}")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if value == 0:
            st.markdown(f"⚪ **{display_name}**: {value}")
        else:
            st.markdown(f"📊 **{display_name}**: {value}")
    elif isinstance(value, str) and value:
        st.markdown(f"📝 **{display_name}**: {value}")
    else:
        st.markdown(f"⚪ **{display_name}**: N/A")


def _is_risky_check(name: str, value: bool) -> bool:
    """Determine if a True/False value is a red flag for this check name."""
    # These checks are risky when True
    risky_when_true = {
        "is_honeypot", "is_mintable", "can_take_back_ownership",
        "has_owner_change_balance", "has_hidden_owner", "is_proxy",
        "has_self_destruct", "has_blacklist_function",
        "has_trading_cooldown", "is_deployer_holding",
        "are_top_holders_contracts", "is_fake_token", "is_airdrop_scam",
    }
    # These checks are risky when False
    risky_when_false = {
        "is_open_source", "lp_locked", "has_website",
        "has_twitter", "has_telegram", "is_on_coingecko",
    }

    if name in risky_when_true:
        return value
    if name in risky_when_false:
        return not value
    return False
