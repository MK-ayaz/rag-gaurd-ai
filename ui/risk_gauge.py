"""Circular risk score gauge — premium Plotly design."""

from __future__ import annotations

import plotly.graph_objects as go


def render_risk_gauge(score: int) -> go.Figure:
    """Create a premium Plotly gauge indicator."""
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
                "font": {"size": 60, "color": bar_color, "family": "Inter, sans-serif", "weight": 700},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#1e293b",
                    "tickfont": {"size": 11, "color": "#475569"},
                },
                "bar": {"color": bar_color, "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(16, 185, 129, 0.06)"},
                    {"range": [30, 50], "color": "rgba(234, 179, 8, 0.06)"},
                    {"range": [50, 70], "color": "rgba(249, 115, 22, 0.06)"},
                    {"range": [70, 100], "color": "rgba(239, 68, 68, 0.06)"},
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
        height=220,
        margin=dict(l=40, r=40, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#ffffff", "family": "Inter, sans-serif"},
    )

    return fig
