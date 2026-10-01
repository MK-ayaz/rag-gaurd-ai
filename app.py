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
        '<div style="font-size:1.3rem; font-weight:700; margin-bottom:12px;">🛡️ About</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "RugGuard AI analyzes any crypto token contract using **4 specialized agents** "
        "and combines their findings into a **0–100 risk score** with a plain-language "
        "AI explanation.",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.85rem; font-weight:600; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">'
        "🔗 Supported Chains</div>",
        unsafe_allow_html=True,
    )
    for key, cfg in CHAINS.items():
        st.markdown(
            f'<div class="chain-pill">'
            f'<span>{cfg["name"]}</span>'
            f'<span style="color:#475569; font-size:0.75rem;">ID {cfg["chain_id"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.85rem; font-weight:600; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">'
        "⚙️ Data Sources</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "- GoPlusLabs (token security)\n"
        "- DexScreener (liquidity & volume)\n"
        "- Honeypot.is (honeypot detection)\n"
        "- CoinGecko (listing verification)\n"
        "- Groq / Llama 3 (AI explanations)",
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_disclaimer()

# Main input
chain_key, address = render_input_section(CHAINS, "ethereum")

# Demo tokens
st.markdown("### 📋 Try a Demo Token")
demo_col1, demo_col2 = st.columns(2)
with demo_col1:
    if st.button("Load USDT (Ethereum)"):
        st.session_state["demo_address"] = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        st.session_state["demo_chain"] = "ethereum"
        st.rerun()
with demo_col2:
    if st.button("Load USDC (Ethereum)"):
        st.session_state["demo_address"] = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        st.session_state["demo_chain"] = "ethereum"

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
        '<p style="text-align:center; color:#64748b; margin-top:2rem; font-size:0.95rem;">'
        "👆 Enter a token contract address above to begin analysis, "
        "or try one of the demo tokens."
        "</p>",
        unsafe_allow_html=True,
    )
