# VisionStat AI Deployment Guide

This guide prepares VisionStat AI for GitHub and Streamlit Cloud deployment.

## Recommended Deployment

Use the lightweight OpenCV version first. It is easier to deploy, reproducible, and does not require model downloads.

## Files Needed

```text
app.py
requirements.txt
.streamlit/config.toml
visionstat/
README.md
AUDIT.md
self_test.py
```

## Streamlit Cloud Steps

1. Create a GitHub repository named `visionstat-ai`.
2. Upload the project files from this folder.
3. Go to Streamlit Cloud.
4. Choose the GitHub repository.
5. Set the main file path to:

```text
app.py
```

6. Deploy the app.
7. Open the deployed URL and test one JPG or PNG image.

## Local Verification Before Deployment

Run:

```bash
pip install -r requirements.txt
python self_test.py
streamlit run app.py
```

Expected self-test result should look similar to:

```text
{'detections': 3, 'quality_score': 57.02, 'decision': 'Review', 'capability': 'Needs review'}
```

## Optional YOLO Deployment

YOLO is optional. The default app uses OpenCV contour-based detection.

If you want deep-learning object detection:

1. Install optional dependencies:

```bash
pip install -r requirements-yolo.txt
```

2. Add a compatible model file such as:

```text
yolov8n.pt
```

3. Enter that model path in the dashboard sidebar.

For public deployments, avoid committing large model files directly to GitHub. Use a release asset, cloud storage, or document that users should provide their own model.

## Common Deployment Issues

### OpenCV install fails

Use `opencv-python-headless`, not `opencv-python`, for Streamlit Cloud.

### App loads but detection labels are generic

That is expected in default mode. OpenCV contour detection finds measurable regions but does not assign semantic object classes.

### YOLO model not found

Confirm the model file exists in the deployed environment and the sidebar path matches the file name.

### Report is HTML, not PDF

The current prototype exports HTML reports. PDF export can be added with a renderer such as WeasyPrint, Playwright, or ReportLab.

## Portfolio Deployment Checklist

- GitHub repository is public
- README explains the default detection method
- App has a live Streamlit URL
- Demo image or screenshot is included in the repository
- Blog post links back to GitHub and live app
- Demo video links back to GitHub and live app
