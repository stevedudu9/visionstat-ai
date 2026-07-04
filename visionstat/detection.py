from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np


def detect_objects(bgr: np.ndarray, model_path: str | None = None, confidence_threshold: float = 0.25) -> tuple[list[dict[str, Any]], str]:
    if model_path:
        yolo_results = try_yolo_detection(bgr, model_path, confidence_threshold)
        if yolo_results is not None:
            return yolo_results, "Ultralytics YOLO"
    return contour_detection(bgr), "OpenCV contour fallback"


def try_yolo_detection(bgr: np.ndarray, model_path: str, confidence_threshold: float) -> list[dict[str, Any]] | None:
    if not Path(model_path).exists():
        return None
    try:
        from ultralytics import YOLO

        model = YOLO(model_path)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        result = model.predict(rgb, conf=confidence_threshold, verbose=False)[0]
    except Exception:
        return None

    detections = []
    names = result.names
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
        cls = int(box.cls[0].item())
        conf = float(box.conf[0].item())
        detections.append(
            {
                "box": [x1, y1, x2, y2],
                "label": names.get(cls, "object"),
                "confidence": conf,
                "area": max(0.0, (x2 - x1) * (y2 - y1)),
            }
        )
    return detections


def contour_detection(bgr: np.ndarray) -> list[dict[str, Any]]:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 120)
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_area = bgr.shape[0] * bgr.shape[1]
    min_area = max(80, image_area * 0.001)
    detections = []
    for contour in contours:
        area = float(cv2.contourArea(contour))
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        extent = area / max(1, w * h)
        confidence = float(np.clip(0.35 + extent * 0.55, 0.2, 0.92))
        detections.append(
            {
                "box": [x, y, x + w, y + h],
                "label": "region",
                "confidence": confidence,
                "area": area,
            }
        )
    detections.sort(key=lambda item: item["area"], reverse=True)
    return detections[:50]


def annotate_image(bgr: np.ndarray, detections: list[dict[str, Any]]) -> np.ndarray:
    annotated = bgr.copy()
    for i, det in enumerate(detections, start=1):
        x1, y1, x2, y2 = [int(v) for v in det["box"]]
        color = (40, 180, 80)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        label = f"{i}: {det.get('label', 'object')} {det.get('confidence', 0):.2f}"
        cv2.putText(annotated, label, (x1, max(18, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
    return annotated
