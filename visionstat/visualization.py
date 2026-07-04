from __future__ import annotations

import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def bgr_to_rgb(bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def quality_gauge(score: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "/100"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 50], "color": "#fee2e2"},
                    {"range": [50, 75], "color": "#fef3c7"},
                    {"range": [75, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10))
    return fig


def measurement_distribution(measurements: pd.DataFrame, metric: str) -> go.Figure:
    fig = px.histogram(measurements, x=metric, nbins=18, marginal="box", color_discrete_sequence=["#0f766e"])
    fig.update_layout(height=330, margin=dict(l=20, r=20, t=30, b=20))
    return fig


def control_chart(chart_data: pd.DataFrame, metric: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_data["sample"], y=chart_data[metric], mode="lines+markers", name=metric))
    for column, label, color in [
        ("center_line", "Center", "#111827"),
        ("ucl", "UCL", "#dc2626"),
        ("lcl", "LCL", "#dc2626"),
        ("warning_high", "Warning", "#f59e0b"),
        ("warning_low", "Warning", "#f59e0b"),
    ]:
        fig.add_trace(go.Scatter(x=chart_data["sample"], y=chart_data[column], mode="lines", name=label, line=dict(color=color, dash="dash")))
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Sample", yaxis_title=metric)
    return fig


def anomaly_heatmap(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Laplacian(gray, cv2.CV_64F)
    heat = cv2.convertScaleAbs(edges)
    heat = cv2.GaussianBlur(heat, (9, 9), 0)
    heat_color = cv2.applyColorMap(cv2.normalize(heat, None, 0, 255, cv2.NORM_MINMAX), cv2.COLORMAP_TURBO)
    overlay = cv2.addWeighted(bgr, 0.62, heat_color, 0.38, 0)
    return overlay
