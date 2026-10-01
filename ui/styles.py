"""Custom CSS for the RugGuard AI modern dark theme."""

CUSTOM_CSS = """
<style>
    /* ── Reset & Base ── */
    .stApp {
        background-color: #06080d;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* ── Typography ── */
    .main-title {
        font-size: 2.75rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.3rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }

    .subtitle {
        font-size: 1.05rem;
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* ── Gradient accent bar ── */
    .accent-bar {
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa, #6366f1);
        background-size: 200% 100%;
        border-radius: 2px;
        margin-bottom: 2rem;
        animation: shimmer 3s ease-in-out infinite;
    }

    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* ── Input card (glass morphism) ── */
    .input-container {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    }

    .input-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    /* ── Chain pills ── */
    .chain-pills {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 8px;
    }

    .chain-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        transition: all 0.2s ease;
        cursor: default;
    }

    .chain-pill.active {
        background: rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
    }

    /* ── Risk score display ── */
    .risk-score-container {
        text-align: center;
        padding: 20px 0;
    }

    .risk-verdict {
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-top: 8px;
        letter-spacing: -0.01em;
    }

    .risk-critical { color: #ef4444; }
    .risk-high { color: #f97316; }
    .risk-medium { color: #eab308; }
    .risk-low { color: #10b981; }

    .token-info {
        text-align: center;
        color: #64748b;
        margin-top: 4px;
        font-size: 0.9rem;
    }

    /* ── Agent cards (modern glass) ── */
    .agent-card {
        background: rgba(17, 24, 39, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .agent-card-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 4px;
        color: #e2e8f0;
    }

    .agent-card-subtitle {
        font-size: 0.75rem;
        color: #64748b;
        margin-bottom: 12px;
    }

    .agent-card-score {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 4px;
        letter-spacing: -0.02em;
    }

    .agent-card-max {
        font-size: 0.75rem;
        color: #475569;
        margin-bottom: 12px;
    }

    .agent-flag {
        font-size: 0.78rem;
        color: #f87171;
        margin-bottom: 4px;
        display: flex;
        align-items: flex-start;
        gap: 6px;
    }

    .agent-flag::before {
        content: "⚠";
        flex-shrink: 0;
    }

    /* ── AI explanation box ── */
    .ai-explanation {
        background: rgba(17, 24, 39, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-left: 3px solid #6366f1;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 10px 0;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #cbd5e1;
    }

    /* ── Section headers ── */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ── Disclaimer ── */
    .disclaimer {
        background: rgba(239, 68, 68, 0.06);
        border: 1px solid rgba(239, 68, 68, 0.15);
        border-left: 3px solid #ef4444;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 2rem;
        font-size: 0.82rem;
        color: #94a3b8;
        line-height: 1.6;
    }

    /* ── Streamlit component overrides ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #f1f5f9;
        padding: 12px 16px;
        font-size: 0.95rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #f1f5f9;
    }

    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    /* ── Divider ── */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
        margin: 24px 0;
    }

    /* ── Metric cards ── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }

    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    .metric-label {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 2px;
    }

    /* ── Status badge ── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .status-badge.success {
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
    }

    .status-badge.error {
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #06080d;
    }

    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }

    /* ── Sidebar overrides ── */
    .stSidebar {
        background: #0a0d14 !important;
    }
</style>
"""


def apply_styles():
    """Apply the custom CSS to the Streamlit app."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def risk_class(score: int) -> str:
    """Return the CSS class name for a given risk score."""
    if score >= 80:
        return "risk-critical"
    elif score >= 60:
        return "risk-high"
    elif score >= 40:
        return "risk-medium"
    else:
        return "risk-low"


def risk_color_hex(score: int) -> str:
    """Return a hex color for a given risk score."""
    if score >= 80:
        return "#ef4444"
    elif score >= 60:
        return "#f97316"
    elif score >= 40:
        return "#eab308"
    else:
        return "#10b981"
