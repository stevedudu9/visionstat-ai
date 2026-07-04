from __future__ import annotations

import numpy as np
import pandas as pd


def control_chart_data(measurements: pd.DataFrame, metric: str = "area_px") -> pd.DataFrame:
    if measurements.empty or metric not in measurements:
        return pd.DataFrame()
    values = measurements[metric].astype(float).dropna().reset_index(drop=True)
    if values.empty:
        return pd.DataFrame()
    mean = values.mean()
    sigma = values.std(ddof=0) or 1.0
    return pd.DataFrame(
        {
            "sample": np.arange(1, len(values) + 1),
            metric: values,
            "center_line": mean,
            "ucl": mean + 3 * sigma,
            "lcl": np.maximum(0, mean - 3 * sigma),
            "warning_high": mean + 2 * sigma,
            "warning_low": np.maximum(0, mean - 2 * sigma),
            "out_of_control": (values > mean + 3 * sigma) | (values < mean - 3 * sigma),
        }
    )


def capability_metrics(measurements: pd.DataFrame, metric: str = "area_px") -> dict[str, float | str]:
    if measurements.empty or metric not in measurements or len(measurements) < 2:
        return {"status": "Insufficient data"}
    values = measurements[metric].astype(float).dropna()
    if len(values) < 2:
        return {"status": "Insufficient data"}
    mean = float(values.mean())
    sigma = float(values.std(ddof=1)) or 1.0
    lsl = max(0.0, mean * 0.75)
    usl = mean * 1.25
    cp = (usl - lsl) / (6 * sigma)
    cpk = min((usl - mean) / (3 * sigma), (mean - lsl) / (3 * sigma))
    return {
        "status": "Stable" if cpk >= 1.0 else "Needs review",
        "mean": round(mean, 2),
        "std_dev": round(sigma, 2),
        "lsl": round(lsl, 2),
        "usl": round(usl, 2),
        "cp": round(float(cp), 3),
        "cpk": round(float(cpk), 3),
    }
