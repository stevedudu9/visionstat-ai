# VisionStat AI

VisionStat AI is a Streamlit computer vision analytics and statistical quality inspection platform. It turns uploaded images into measurable quality, detection, defect, anomaly, and process-control insights.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://visionstat-ai-4qwnrvlv74yzaxd2yi4a97.streamlit.app/)

Live app: https://visionstat-ai-4qwnrvlv74yzaxd2yi4a97.streamlit.app/

## Features

- Image upload, preview, validation, and metadata summary
- Brightness, contrast, sharpness, blur, noise, and resolution quality scoring
- Object detection with a contour-based fallback and optional Ultralytics YOLO support
- Statistical measurements for detected regions
- Quality inspection with pass/fail decision and defect localization
- Anomaly scoring and visual heatmap
- SPC dashboard with control limits and process capability estimates
- Explainable AI style overlays and confidence summaries
- Downloadable HTML report

## Current Detection Method

By default, VisionStat AI uses OpenCV contour-based detection to remain lightweight and reproducible. If a compatible YOLO model is provided by the user, the application can optionally perform deep-learning-based object detection.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit and upload a JPG, PNG, JPEG, or BMP image.

If another Streamlit app is already using the default port, run:

```bash
streamlit run app.py --server.port 8517
```

## Deploy On Streamlit Cloud

The app is deployed on Streamlit Cloud. To redeploy or recreate it, use these settings:

- Repository: `stevedudu9/visionstat-ai`
- Branch: `main`
- Main file path: `app.py`
- Dependency file: `requirements.txt`

The default deployment uses OpenCV contour-based detection. YOLO is optional and should only be enabled if you provide a compatible model file and install `requirements-yolo.txt`.

## Self-Test

Run the built-in audit smoke test:

```bash
python self_test.py
```

## Portfolio Materials

- `DEPLOYMENT.md`: Streamlit Cloud and GitHub deployment guide
- `DEMO_VIDEO_SCRIPT.md`: 60-90 second demo script, recording plan, and LinkedIn caption
- `TECHNICAL_BLOG_POST.md`: portfolio-ready technical article
- `INTERVIEW_PREP.md`: project explanation, likely questions, and strong answers
- `AUDIT.md`: verification notes, fixes, and known limits

## Optional YOLO Support

To enable YOLO detection, install the optional dependencies and place a compatible model file such as `yolov8n.pt` in this folder. The app will use it automatically when available.

```bash
pip install -r requirements-yolo.txt
```

## Project Structure

```text
visionstat_ai/
  app.py
  AUDIT.md
  DEPLOYMENT.md
  DEMO_VIDEO_SCRIPT.md
  INTERVIEW_PREP.md
  requirements.txt
  requirements-yolo.txt
  TECHNICAL_BLOG_POST.md
  visionstat/
    analysis.py
    detection.py
    reporting.py
    spc.py
    visualization.py
```

## Notes

This project is designed as a professional prototype. For regulated production use, validation datasets, calibrated thresholds, model governance, audit logs, and domain-specific acceptance criteria should be added.
