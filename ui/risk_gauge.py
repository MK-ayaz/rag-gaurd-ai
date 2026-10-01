"""Circular risk score gauge using Plotly."""

from __future__ import annotations

import plotly.graph_objects as go


def render_risk_gauge(score: int) -> go.Figure:
    """Create a modern Plotly gauge indicator for the overall risk score."""
    if score >= 80:
        bar_color = "#ef4444"
    elif score >= 60:
        bar_color = "#f97316"
    elif score >= 40:
        bar_color = "#eab308"
    else:
        bar_color = "#10b981"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": "/100",
                "font": {"size": 56, "color": bar_color, "family": "Inter, sans-serif"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#334155",
                    "tickfont": {"size": 11, "color": "#64748b"},
                },
                "bar": {"color": bar_color, "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(16, 185, 129, 0.08)"},
                    {"range": [30, 50], "color": "rgba(234, 179, 8, 0.08)"},
                    {"range": [50, 70], "color": "rgba(249, 115, 22, 0.08)"},
                    {"range": [70, 100], "color": "rgba(239, 68, 68, 0.08)"},
                ],
                "threshold": {
                    "line": {"color": bar_color, "width": 3},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        height=240,
        margin=dict(l=30, r=30, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#ffffff", "family": "Inter, sans-serif"},
    )

    return fig
