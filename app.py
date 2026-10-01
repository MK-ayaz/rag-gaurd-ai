"""RugGuard AI — Token Scam & Honeypot Detector.

Main Streamlit entry point. Paste a token contract address, select a chain,
and get an instant scam risk score powered by 4 analysis agents + AI summary.
"""

from __future__ import annotations

import streamlit as st

from config import CHAINS
from utils.validators import is_solana_tx, is_tx_hash, normalize_address, validate_address, validate_chain
from agents.orchestrator import RugGuardOrchestrator
from ui.styles import apply_styles
from ui.icons import ICON_CHAIN, ICON_DEMO, ICON_SOURCE, ICON_SETTINGS, ICON_SHIELD
from ui.dashboard import (
    render_header,
    render_input_section,
    render_full_report,
    render_disclaimer,
)

st.set_page_config(
    page_title="RugGuard AI — Token Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_styles()
render_header()

# Sidebar
with st.sidebar:
    st.markdown(
        f'<div style="font-size:1.1rem; font-weight:700; margin-bottom:10px; color:#e2e8f0; display:flex; align-items:center; gap:8px;">'
        f'{ICON_SHIELD} About RugGuard AI</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "Analyzes any token contract using **4 AI agents** and returns a "
        "**0–100 risk score** with a plain-language AI explanation.",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="font-size:0.75rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px; display:flex; align-items:center; gap:6px;">'
        f'{ICON_CHAIN} Chains</div>',
        unsafe_allow_html=True,
    )
    for key, cfg in CHAINS.items():
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:8px; padding:5px 0; font-size:0.82rem;">'
            f'<span style="color:#e2e8f0; font-weight:500;">{cfg["name"]}</span>'
            f'<span style="color:#334155; font-size:0.7rem;">{cfg["native_currency"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="font-size:0.75rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px; display:flex; align-items:center; gap:6px;">'
        f'{ICON_SETTINGS} Data Sources</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<span style='font-size:0.78rem; color:#475569; line-height:1.6;'>"
        "GoPlusLabs · DexScreener · Honeypot.is · CoinGecko · Groq"
        "</span>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    render_disclaimer()

# Main input
chain_key, address = render_input_section(CHAINS, "ethereum")

# Demo tokens
st.markdown(
    f'<div style="text-align:center; margin-top:20px; margin-bottom:12px;">'
    f'<span style="font-size:0.8rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.06em; display:inline-flex; align-items:center; gap:6px;">'
    f'{ICON_DEMO} Quick Demo</span>'
    f'</div>',
    unsafe_allow_html=True,
)
demo_col1, demo_col2, demo_col3 = st.columns(3)
with demo_col1:
    if st.button("USDT · ETH", width="stretch"):
        st.session_state["demo_address"] = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        st.session_state["demo_chain"] = "ethereum"
        st.rerun()
with demo_col2:
    if st.button("USDC · ETH", width="stretch"):
        st.session_state["demo_address"] = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        st.session_state["demo_chain"] = "ethereum"
        st.rerun()
with demo_col3:
    if st.button("USDT · BSC", width="stretch"):
        st.session_state["demo_address"] = "0x55d398326f99059ff775485246999027b3197955"
        st.session_state["demo_chain"] = "bsc"
        st.rerun()

# Handle demo button loading
if "demo_address" in st.session_state:
    address = st.session_state["demo_address"]
    chain_key = st.session_state.get("demo_chain", "ethereum")
    del st.session_state["demo_address"]
    if "demo_chain" in st.session_state:
        del st.session_state["demo_chain"]

# Validation and analysis
if address:
    normalized = normalize_address(address)
    if not normalized:
        st.error(
            "❌ That does not look like a token contract address. "
            "Paste the token's contract address, like "
            "`0x5CF00327Edb646632BB69f1D3C38224685AEEb31`, or an explorer URL "
            "containing one (Etherscan, BscScan, PolygonScan, Solscan). "
            "Do not paste a wallet address, profile, or transaction hash."
        )
    elif is_tx_hash(normalized):
        st.error(
            "❌ That looks like a transaction hash, not a token contract address. "
            "Transaction hashes are 64 characters; contract addresses are 40. "
            "On your explorer, find the **Token Contract** address instead."
        )
    elif is_solana_tx(normalized):
        st.error(
            "❌ That looks like a Solana transaction signature, not a token contract address. "
            "Transaction signatures are 87-88 characters; contract addresses are 43-44. "
            "On Solscan, find the **Token Account** address instead."
        )
    elif not validate_address(normalized):
        st.error(
            "❌ That does not look like a token contract address. "
            "A valid EVM contract address starts with '0x' followed by 40 hexadecimal characters. "
            "A Solana token account address is 43-44 Base58 characters. "
            "Do not paste a wallet address, profile, or transaction hash."
        )
    elif not validate_chain(chain_key):
        st.error(f"❌ Unsupported chain. Supported chains: {', '.join(CHAINS.keys())}")
    else:
        orchestrator = RugGuardOrchestrator(normalized, chain_key)

        with st.spinner("🔍 Analyzing token..."):
            status = st.empty()
            status.info("Running Contract Auditor...")
            report = orchestrator.run_analysis(use_ai=True)
            status.success("Analysis complete!")

        if report.final_score >= 80:
            st.error(f"🚨 {report.verdict}")
        elif report.final_score >= 60:
            st.warning(f"⚠️ {report.verdict}")
        elif report.final_score >= 40:
            st.warning(f"🟡 {report.verdict}")
        elif report.final_score >= 20:
            st.success(f"🟢 {report.verdict}")
        else:
            st.success(f"✅ {report.verdict}")

        render_full_report(report)
else:
    st.markdown(
        '<div class="empty-state">'
        '<div class="empty-state-icon">🔍</div>'
        '<div class="empty-state-text">Enter a token contract address above to begin analysis, '
        'or try a demo token.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
