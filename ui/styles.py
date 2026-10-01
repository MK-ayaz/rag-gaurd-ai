"""RugGuard AI — Modern Branded UI Styles.

Design system inspired by premium security/analytics products:
- Deep navy background with subtle noise texture
- Indigo/violet brand gradient
- Glass-morphism cards with refined borders
- Consistent spacing, typography, and component shapes
- Professional micro-interactions via CSS
"""

CUSTOM_CSS = """
<style>
    /* ═══════════════════════════════════════════
       BASE & RESET
       ═══════════════════════════════════════════ */
    .stApp {
        background-color: #06080d;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    *, *::before, *::after {
        box-sizing: border-box;
    }

    /* ═══════════════════════════════════════════
       BRAND & HERO
       ═══════════════════════════════════════════ */
    .brand-container {
        text-align: center;
        padding: 40px 20px 32px;
        position: relative;
    }

    .brand-logo {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
        font-size: 2rem;
    }

    .brand-name {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #e0e7ff 0%, #c4b5fd 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .brand-tagline {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 400;
        letter-spacing: 0.02em;
    }

    .brand-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(99,102,241,0.3) 50%, transparent 100%);
        margin: 24px auto;
        max-width: 400px;
    }

    /* ═══════════════════════════════════════════
       SEARCH / INPUT SECTION
       ═══════════════════════════════════════════ */
    .search-card {
        max-width: 720px;
        margin: 0 auto 32px;
        padding: 28px;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .search-row {
        display: flex;
        gap: 12px;
        align-items: flex-end;
    }

    .search-field {
        flex: 1;
    }

    .search-field-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
        display: block;
    }

    .search-btn {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 11px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease !important;
        white-space: nowrap;
    }

    .search-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.5) !important;
    }

    /* ═══════════════════════════════════════════
       ERROR MESSAGES
       ═══════════════════════════════════════════ */
    .error-card {
        max-width: 720px;
        margin: 0 auto 20px;
        padding: 14px 20px;
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 12px;
        font-size: 0.88rem;
        color: #fca5a5;
        line-height: 1.6;
    }

    /* ═══════════════════════════════════════════
       LOADING STATE
       ═══════════════════════════════════════════ */
    .loading-container {
        max-width: 720px;
        margin: 24px auto;
        padding: 24px;
        text-align: center;
    }

    .loading-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid rgba(99, 102, 241, 0.15);
        border-top-color: #6366f1;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .loading-text {
        margin-top: 12px;
        font-size: 0.85rem;
        color: #64748b;
    }

    /* ═══════════════════════════════════════════
       RESULTS DASHBOARD
       ═══════════════════════════════════════════ */
    .results-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 0 16px;
    }

    .results-header {
        text-align: center;
        padding: 24px 0 16px;
    }

    /* ── Risk Gauge Section ── */
    .gauge-section {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 20px;
        padding: 32px 24px;
        margin-bottom: 24px;
        text-align: center;
        backdrop-filter: blur(10px);
    }

    .risk-verdict {
        font-size: 1.75rem;
        font-weight: 800;
        text-align: center;
        margin-top: 8px;
        letter-spacing: -0.02em;
    }

    .risk-critical { color: #ef4444; }
    .risk-high { color: #f97316; }
    .risk-medium { color: #eab308; }
    .risk-low { color: #10b981; }

    .token-meta {
        text-align: center;
        color: #64748b;
        margin-top: 6px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* ── Agent Cards Grid ── */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }

    @media (max-width: 900px) {
        .agent-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    .agent-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    .agent-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--agent-color);
        opacity: 0.6;
        transition: opacity 0.2s ease;
    }

    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.08);
    }

    .agent-card:hover::before {
        opacity: 1;
    }

    .agent-card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }

    .agent-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }

    .agent-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #e2e8f0;
        line-height: 1.2;
    }

    .agent-subtitle {
        font-size: 0.7rem;
        color: #475569;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .agent-score {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-bottom: 4px;
    }

    .agent-score-max {
        font-size: 0.75rem;
        color: #334155;
        font-weight: 500;
        margin-bottom: 12px;
    }

    .agent-bar-track {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 3px;
        height: 5px;
        overflow: hidden;
        margin-bottom: 12px;
    }

    .agent-bar-fill {
        height: 5px;
        border-radius: 3px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .agent-flags {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .agent-flag {
        font-size: 0.75rem;
        color: #f87171;
        line-height: 1.4;
        padding-left: 14px;
        position: relative;
    }

    .agent-flag::before {
        content: "⚠";
        position: absolute;
        left: 0;
        top: 0;
        font-size: 0.7rem;
    }

    .agent-error {
        font-size: 0.75rem;
        color: #64748b;
        line-height: 1.4;
        margin-top: 4px;
    }

    /* ── AI Section ── */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        margin: 28px 0;
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .ai-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-left: 3px solid #6366f1;
        border-radius: 14px;
        padding: 20px 24px;
        font-size: 0.92rem;
        line-height: 1.75;
        color: #cbd5e1;
    }

    /* ── Detailed Findings ── */
    .finding-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        margin-bottom: 12px;
        overflow: hidden;
    }

    .finding-header {
        padding: 14px 18px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #e2e8f0;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: background 0.15s ease;
    }

    .finding-header:hover {
        background: rgba(255, 255, 255, 0.02);
    }

    .finding-body {
        padding: 0 18px 16px;
    }

    .finding-flag {
        color: #f87171;
        font-size: 0.82rem;
        margin-bottom: 10px;
        line-height: 1.5;
    }

    .check-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 5px 0;
        font-size: 0.82rem;
    }

    .check-icon {
        width: 18px;
        text-align: center;
        flex-shrink: 0;
    }

    .check-label {
        color: #64748b;
        flex-shrink: 0;
    }

    .check-value {
        font-weight: 500;
        color: #e2e8f0;
    }

    .check-value.danger {
        color: #ef4444;
    }

    .check-value.safe {
        color: #10b981;
    }

    /* ── Disclaimer ── */
    .disclaimer {
        background: rgba(239, 68, 68, 0.04);
        border: 1px solid rgba(239, 68, 68, 0.1);
        border-left: 3px solid #ef4444;
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 32px;
        font-size: 0.78rem;
        color: #64748b;
        line-height: 1.65;
    }

    .disclaimer strong {
        color: #94a3b8;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 48px 20px;
        color: #334155;
    }

    .empty-state-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
        opacity: 0.6;
    }

    .empty-state-text {
        font-size: 0.9rem;
        color: #475569;
    }

    /* ═══════════════════════════════════════════
       STREAMLIT OVERRIDES
       ═══════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 11px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.45) !important;
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 11px 16px !important;
        font-size: 0.9rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08) !important;
    }

    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }

    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }

    .stSpinner > div {
        border-color: rgba(99, 102, 241, 0.15) !important;
        border-top-color: #6366f1 !important;
    }

    /* Hide streamlit default elements */
    footer, #MainMenu {
        visibility: hidden !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }
</style>
"""


def apply_styles():
    """Apply the custom CSS to the Streamlit app."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def risk_class(score: int) -> str:
    if score >= 80:
        return "risk-critical"
    elif score >= 60:
        return "risk-high"
    elif score >= 40:
        return "risk-medium"
    else:
        return "risk-low"


def risk_color_hex(score: int) -> str:
    if score >= 80:
        return "#ef4444"
    elif score >= 60:
        return "#f97316"
    elif score >= 40:
        return "#eab308"
    else:
        return "#10b981"
