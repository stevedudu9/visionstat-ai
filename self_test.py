from __future__ import annotations

import sys

import cv2
import numpy as np
from PIL import Image

from visionstat.analysis import (
    anomaly_scores,
    assess_quality,
    image_metadata,
    inspect_quality,
    measure_regions,
    pil_to_bgr,
)
from visionstat.detection import annotate_image, detect_objects
from visionstat.reporting import build_html_report
from visionstat.spc import capability_metrics, control_chart_data
from visionstat.visualization import anomaly_heatmap, bgr_to_rgb, control_chart, measurement_distribution, quality_gauge


def synthetic_image() -> np.ndarray:
    image = np.full((360, 480, 3), 36, dtype=np.uint8)
    cv2.rectangle(image, (55, 70), (170, 245), (220, 220, 220), -1)
    cv2.circle(image, (315, 160), 62, (70, 170, 235), -1)
    cv2.rectangle(image, (380, 260), (445, 325), (190, 80, 80), -1)
    return image


def main() -> int:
    bgr = synthetic_image()
    pil_image = Image.fromarray(bgr_to_rgb(bgr))
    metadata = image_metadata(pil_image, "synthetic.png", 4096)
    round_trip = pil_to_bgr(pil_image)
    quality = assess_quality(round_trip)
    detections, detector_name = detect_objects(round_trip, model_path="missing-model.pt")
    measurements = anomaly_scores(measure_regions(round_trip, detections))
    inspection = inspect_quality(measurements, quality)
    chart_data = control_chart_data(measurements)
    capability = capability_metrics(measurements)
    annotated = annotate_image(round_trip, detections)
    heatmap = anomaly_heatmap(round_trip)
    report = build_html_report(metadata, quality, inspection, detections, measurements, capability)

    assert detector_name == "OpenCV contour fallback"
    assert quality["quality_score"] >= 0
    assert annotated.shape == bgr.shape
    assert heatmap.shape == bgr.shape
    assert "VisionStat AI Inspection Report" in report
    assert "anomaly_score" in measurements.columns or measurements.empty
    if not measurements.empty:
        assert not measurements["anomaly_score"].isna().any()
        measurement_distribution(measurements, "area_px")
    if not chart_data.empty:
        control_chart(chart_data, "area_px")
    quality_gauge(quality["quality_score"])

    print(
        {
            "detections": len(detections),
            "quality_score": round(quality["quality_score"], 2),
            "decision": inspection["decision"],
            "capability": capability.get("status"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
