from __future__ import annotations

from html import escape
from typing import Any

import pandas as pd


def build_html_report(
    metadata: Any,
    quality: dict[str, Any],
    inspection: dict[str, Any],
    detections: list[dict[str, Any]],
    measurements: pd.DataFrame,
    capability: dict[str, Any],
) -> str:
    measurement_html = measurements.to_html(index=False, classes="table") if not measurements.empty else "<p>No measurements available.</p>"
    recommendations = "".join(f"<li>{escape(item)}</li>" for item in quality["recommendations"])
    issues = "".join(f"<li>{escape(item)}</li>" for item in inspection["issues"])
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>VisionStat AI Inspection Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #111827; }}
    h1, h2 {{ color: #0f172a; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .card {{ border: 1px solid #d1d5db; border-radius: 8px; padding: 14px; }}
    .metric {{ font-size: 28px; font-weight: 700; }}
    .table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
    .table th, .table td {{ border: 1px solid #d1d5db; padding: 6px 8px; text-align: right; }}
    .table th:first-child, .table td:first-child, .table th:nth-child(2), .table td:nth-child(2) {{ text-align: left; }}
  </style>
</head>
<body>
  <h1>VisionStat AI Inspection Report</h1>
  <p>Image: <strong>{escape(metadata.filename)}</strong> | {metadata.width} x {metadata.height} | {metadata.file_size_kb} KB | {escape(metadata.format)}</p>
  <div class="grid">
    <div class="card"><div>Quality Score</div><div class="metric">{quality["quality_score"]:.1f}/100</div></div>
    <div class="card"><div>Inspection Decision</div><div class="metric">{escape(inspection["decision"])}</div></div>
    <div class="card"><div>Detected Objects</div><div class="metric">{len(detections)}</div></div>
  </div>
  <h2>Quality Assessment</h2>
  <ul>{recommendations}</ul>
  <h2>Inspection Findings</h2>
  <ul>{issues}</ul>
  <h2>Process Capability</h2>
  <pre>{escape(str(capability))}</pre>
  <h2>Measurements</h2>
  {measurement_html}
</body>
</html>"""
