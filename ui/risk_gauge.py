"""Circular risk score gauge using Plotly."""

from __future__ import annotations

import plotly.graph_objects as go


def render_risk_gauge(score: int) -> go.Figure:
    """Create a Plotly gauge indicator for the overall risk score."""
    if score >= 80:
        bar_color = "#ff4b4b"
    elif score >= 60:
        bar_color = "#ff8c00"
    elif score >= 40:
        bar_color = "#ffd700"
    else:
        bar_color = "#00e676"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            number={"suffix": "/100", "font": {"size": 48, "color": bar_color}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#666",
                    "tickfont": {"size": 12, "color": "#aaa"},
                },
                "bar": {"color": bar_color, "thickness": 0.35},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 1,
                "bordercolor": "#333",
                "steps": [
                    {"range": [0, 30], "color": "rgba(0, 230, 118, 0.15)"},
                    {"range": [30, 50], "color": "rgba(255, 215, 0, 0.15)"},
                    {"range": [50, 70], "color": "rgba(255, 140, 0, 0.15)"},
                    {"range": [70, 100], "color": "rgba(255, 75, 75, 0.15)"},
                ],
                "threshold": {
                    "line": {"color": bar_color, "width": 4},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#ffffff"},
    )

    return fig
