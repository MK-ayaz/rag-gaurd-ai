"""Custom CSS for the RugGuard AI dark theme."""

CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #0e1117;
    }

    /* Main title */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.1rem;
        text-align: center;
        color: #a0a0b0;
        margin-bottom: 1.5rem;
    }

    /* Risk score verdict */
    .risk-critical {
        color: #ff4b4b;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .risk-high {
        color: #ff8c00;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .risk-medium {
        color: #ffd700;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .risk-low {
        color: #00e676;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }

    /* Agent cards */
    .agent-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #333;
        height: 100%;
    }
    .agent-card-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #e0e0f0;
    }
    .agent-card-score {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }
    .agent-flag {
        font-size: 0.8rem;
        color: #ff6b6b;
        margin-bottom: 0.2rem;
    }

    /* AI explanation box */
    .ai-explanation {
        background: #1a1a2e;
        border: 1px solid #4a4a6a;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }

    /* Input area */
    .input-container {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #333;
        margin-bottom: 1.5rem;
    }

    /* Disclaimer */
    .disclaimer {
        background: #1a1a1a;
        border-left: 4px solid #ff4b4b;
        border-radius: 4px;
        padding: 12px 16px;
        margin-top: 2rem;
        font-size: 0.85rem;
        color: #c0c0d0;
    }

    /* Status indicators */
    .status-ok { color: #00e676; }
    .status-bad { color: #ff4b4b; }
    .status-warn { color: #ffd700; }

    /* Metric value overrides */
    .stMetric > label {
        color: #a0a0b0;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1e1e2e;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
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
        return "#ff4b4b"
    elif score >= 60:
        return "#ff8c00"
    elif score >= 40:
        return "#ffd700"
    else:
        return "#00e676"
