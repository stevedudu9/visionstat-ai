from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ImageMetadata:
    filename: str
    width: int
    height: int
    channels: int
    file_size_kb: float
    mode: str
    format: str


def pil_to_bgr(image: Any) -> np.ndarray:
    rgb = np.array(image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def image_metadata(image: Any, filename: str, file_size: int) -> ImageMetadata:
    width, height = image.size
    channels = len(image.getbands())
    return ImageMetadata(
        filename=filename,
        width=width,
        height=height,
        channels=channels,
        file_size_kb=round(file_size / 1024, 2),
        mode=image.mode,
        format=image.format or "Unknown",
    )


def assess_quality(bgr: np.ndarray) -> dict[str, Any]:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    brightness = float(np.mean(gray))
    contrast = float(np.std(gray))
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    blur_index = max(0.0, 100.0 - min(100.0, sharpness / 5.0))
    noise = estimate_noise(gray)
    resolution_mp = (height * width) / 1_000_000

    brightness_score = score_range(brightness, 85, 185, 35, 225)
    contrast_score = score_minimum(contrast, 45, 90)
    sharpness_score = score_minimum(sharpness, 120, 600)
    noise_score = 100 - score_minimum(noise, 18, 55)
    resolution_score = score_minimum(resolution_mp, 0.35, 2.0)
    quality_score = float(
        np.average(
            [brightness_score, contrast_score, sharpness_score, noise_score, resolution_score],
            weights=[0.2, 0.22, 0.28, 0.15, 0.15],
        )
    )

    recommendations = []
    if brightness_score < 70:
        recommendations.append("Improve lighting or exposure before inspection.")
    if contrast_score < 70:
        recommendations.append("Increase scene contrast or use a more controlled background.")
    if sharpness_score < 70:
        recommendations.append("Retake the image with better focus or a faster shutter speed.")
    if noise_score < 70:
        recommendations.append("Reduce sensor noise with stronger lighting or lower ISO.")
    if resolution_score < 70:
        recommendations.append("Use a higher-resolution image for more reliable measurements.")
    if not recommendations:
        recommendations.append("Image quality is suitable for automated inspection.")

    return {
        "brightness": brightness,
        "contrast": contrast,
        "sharpness": sharpness,
        "blur_index": blur_index,
        "noise": noise,
        "resolution_mp": resolution_mp,
        "quality_score": quality_score,
        "recommendations": recommendations,
    }


def estimate_noise(gray: np.ndarray) -> float:
    median = cv2.medianBlur(gray, 3)
    residual = cv2.absdiff(gray, median)
    return float(np.std(residual))


def score_range(value: float, good_low: float, good_high: float, hard_low: float, hard_high: float) -> float:
    if good_low <= value <= good_high:
        return 100.0
    if value < good_low:
        return float(np.clip(100 * (value - hard_low) / (good_low - hard_low), 0, 100))
    return float(np.clip(100 * (hard_high - value) / (hard_high - good_high), 0, 100))


def score_minimum(value: float, weak: float, strong: float) -> float:
    return float(np.clip(100 * (value - weak) / (strong - weak), 0, 100))


def measure_regions(bgr: np.ndarray, detections: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    image_height, image_width = bgr.shape[:2]
    for i, det in enumerate(detections, start=1):
        x1, y1, x2, y2 = [int(v) for v in det["box"]]
        x1 = int(np.clip(x1, 0, image_width - 1))
        x2 = int(np.clip(x2, 0, image_width))
        y1 = int(np.clip(y1, 0, image_height - 1))
        y2 = int(np.clip(y2, 0, image_height))
        if x2 <= x1 or y2 <= y1:
            continue
        crop = bgr[y1:y2, x1:x2]
        if crop.size == 0:
            continue
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area = float(det.get("area", (x2 - x1) * (y2 - y1)))
        perimeter = 0.0
        circularity = 0.0
        if contours:
            contour = max(contours, key=cv2.contourArea)
            perimeter = float(cv2.arcLength(contour, True))
            contour_area = float(cv2.contourArea(contour))
            if perimeter > 0:
                circularity = float((4 * np.pi * contour_area) / (perimeter**2))
        mean_bgr = np.mean(crop.reshape(-1, 3), axis=0)
        rows.append(
            {
                "id": i,
                "label": det.get("label", "object"),
                "confidence": round(float(det.get("confidence", 0.0)), 3),
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "area_px": round(area, 2),
                "perimeter_px": round(perimeter, 2),
                "aspect_ratio": round((x2 - x1) / max(1, y2 - y1), 3),
                "circularity": round(circularity, 3),
                "mean_red": round(float(mean_bgr[2]), 2),
                "mean_green": round(float(mean_bgr[1]), 2),
                "mean_blue": round(float(mean_bgr[0]), 2),
            }
        )
    return pd.DataFrame(rows)


def inspect_quality(measurements: pd.DataFrame, quality: dict[str, Any]) -> dict[str, Any]:
    issues = []
    defect_rate = 0.0

    if quality["quality_score"] < 70:
        issues.append("Image acquisition quality is below the recommended inspection threshold.")
    if measurements.empty:
        issues.append("No measurable objects were detected.")
    else:
        area = measurements["area_px"]
        z = (area - area.mean()) / max(area.std(ddof=0), 1)
        outliers = measurements.loc[z.abs() > 2.5, "id"].tolist()
        if outliers:
            issues.append(f"Size deviation detected in object IDs: {', '.join(map(str, outliers))}.")
        color_spread = measurements[["mean_red", "mean_green", "mean_blue"]].std(ddof=0).mean()
        if color_spread > 45:
            issues.append("Color inconsistency is high across detected objects.")
        defect_rate = min(100.0, (len(outliers) / max(1, len(measurements))) * 100)

    decision = "Pass" if not issues else "Review"
    if quality["quality_score"] < 50 or (not measurements.empty and defect_rate > 20):
        decision = "Fail"

    return {
        "decision": decision,
        "defect_rate": defect_rate,
        "issues": issues or ["No major inspection issues detected."],
    }


def anomaly_scores(measurements: pd.DataFrame) -> pd.DataFrame:
    if measurements.empty:
        return measurements
    features = measurements[["area_px", "aspect_ratio", "circularity", "mean_red", "mean_green", "mean_blue"]].copy()
    zscores = (features - features.mean()) / features.std(ddof=0).replace(0, 1)
    zscores = zscores.replace([np.inf, -np.inf], 0).fillna(0)
    scored = measurements.copy()
    scored["anomaly_score"] = zscores.abs().mean(axis=1).round(3)
    scored["anomaly_flag"] = scored["anomaly_score"] > 1.25
    return scored
