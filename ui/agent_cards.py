"""Agent result cards — one per analysis agent."""

from __future__ import annotations

import streamlit as st

from models.risk_report import AgentResult, RiskReport
from ui.styles import risk_class, risk_color_hex

AGENT_META = [
    ("contract", "🔍 Contract Auditor", "Smart contract security", "#6366f1"),
    ("liquidity", "💧 Liquidity Agent", "LP lock & depth", "#06b6d4"),
    ("holder", "👥 Holder Agent", "Holder concentration", "#10b981"),
    ("social", "🌐 Social Agent", "Social presence", "#f59e0b"),
]


def _render_score_bar(score: int, color: str) -> str:
    """Render a horizontal progress bar for the agent score."""
    pct = max(0, min(100, score))
    return (
        f'<div style="background: rgba(255,255,255,0.06); border-radius: 4px; height: 6px; margin-top: 8px;">'
        f'<div style="background: {color}; border-radius: 4px; height: 6px; width: {pct}%; transition: width 0.4s ease;"></div>'
        f'</div>'
    )


def render_agent_cards(report: RiskReport) -> None:
    """Render the 4 agent result cards in a responsive grid."""
    cols = st.columns(4)

    for idx, (agent_key, title, subtitle, accent) in enumerate(AGENT_META):
        result: AgentResult | None = report.agent_results.get(agent_key)
        with cols[idx]:
            if result is None:
                st.markdown(
                    f'<div class="agent-card" style="text-align:center;">'
                    f'<div class="agent-card-title">{title}</div>'
                    f'<div style="color:#64748b; font-size:0.85rem;">No data</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                continue

            color = risk_color_hex(result.risk_score)

            if result.has_error():
                st.markdown(
                    f'<div class="agent-card">'
                    f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">'
                    f'<div style="width:32px; height:32px; border-radius:8px; background:rgba(239,68,68,0.1); display:flex; align-items:center; justify-content:center;">'
                    f'<span style="font-size:1rem;">⚠</span></div>'
                    f'<div><div class="agent-card-title">{title}</div>'
                    f'<div class="agent-card-subtitle">{subtitle}</div></div>'
                    f'</div>'
                    f'<div class="agent-card-score" style="color: #475569;">N/A</div>'
                    f'<div style="font-size:0.78rem; color:#f87171; margin-top:8px;">'
                    f'{result.error[:80]}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                flags_html = ""
                for flag in result.red_flags[:2]:
                    flags_html += f'<div class="agent-flag">{flag}</div>'

                st.markdown(
                    f'<div class="agent-card">'
                    f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">'
                    f'<div style="width:32px; height:32px; border-radius:8px; background:{color}15; display:flex; align-items:center; justify-content:center;">'
                    f'<span style="font-size:1rem;">{title[0]}</span></div>'
                    f'<div><div class="agent-card-title">{title}</div>'
                    f'<div class="agent-card-subtitle">{subtitle}</div></div>'
                    f'</div>'
                    f'<div class="agent-card-score" style="color: {color};">{result.risk_score}<span style="font-size:0.9rem; font-weight:400; color:#475569;">/100</span></div>'
                    f'{_render_score_bar(result.risk_score, color)}'
                    f'<div style="margin-top:10px;">{flags_html}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Expandable details
                with st.expander("Details", expanded=False):
                    for check_name, check_val in result.checks.items():
                        if check_name in ("owner_address", "website_url", "twitter_url", "telegram_url"):
                            continue
                        _render_check_row(check_name, check_val)


def _render_check_row(name: str, value) -> None:
    """Render a single check as a row with icon."""
    display_name = name.replace("_", " ").title()

    if isinstance(value, bool):
        icon = "✅" if not _is_risky_check(name, value) else "❌"
        color = "#10b981" if not _is_risky_check(name, value) else "#ef4444"
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:8px; padding:4px 0; font-size:0.85rem;">'
            f'<span>{icon}</span>'
            f'<span style="color:#94a3b8;">{display_name}:</span>'
            f'<span style="color: {color}; font-weight:600;">{"Yes" if value else "No"}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        color = "#ef4444" if value != 0 else "#64748b"
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:8px; padding:4px 0; font-size:0.85rem;">'
            f'<span>📊</span>'
            f'<span style="color:#94a3b8;">{display_name}:</span>'
            f'<span style="color: {color}; font-weight:600;">{value:,.2f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    elif isinstance(value, str) and value:
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:8px; padding:4px 0; font-size:0.85rem;">'
            f'<span>📝</span>'
            f'<span style="color:#94a3b8;">{display_name}:</span>'
            f'<span style="color:#e2e8f0; font-weight:500;">{value}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:8px; padding:4px 0; font-size:0.85rem;">'
            f'<span>⚪</span>'
            f'<span style="color:#94a3b8;">{display_name}:</span>'
            f'<span style="color:#475569;">N/A</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _is_risky_check(name: str, value: bool) -> bool:
    """Determine if a True/False value is a red flag for this check name."""
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
