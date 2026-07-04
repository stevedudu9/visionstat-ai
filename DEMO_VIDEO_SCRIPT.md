# VisionStat AI Demo Video Script

Target length: 60-90 seconds

## Video Goal

Show that VisionStat AI turns an uploaded image into measurable computer vision and statistical quality insights.

## Recording Setup

- Open the Streamlit app.
- Use one clear sample image with several visible objects or regions.
- Keep the browser zoom at 100%.
- Record the full browser window.
- Export as MP4 for LinkedIn, GitHub README, or portfolio use.

## 60-90 Second Voiceover

Hi, this is VisionStat AI, a computer vision analytics and statistical quality inspection platform built with Streamlit, OpenCV, Pandas, and Plotly.

The goal is to convert visual information into measurable quality data. I start by uploading an inspection image. The app validates the image, shows its metadata, and calculates quality indicators such as brightness, contrast, sharpness, blur, noise, and resolution.

By default, the app uses OpenCV contour-based detection so it stays lightweight and reproducible. If a YOLO model is provided, it can optionally switch to deep-learning-based object detection.

After detection, VisionStat AI measures each region, including area, width, height, perimeter, aspect ratio, circularity, and color statistics. These measurements feed into the inspection logic, anomaly scoring, and statistical process control charts.

The dashboard gives a clear inspection decision, shows potential defects or unusual regions, and visualizes process stability using control limits and capability metrics.

Finally, the user can download an HTML report containing the image summary, quality assessment, measurements, inspection results, SPC findings, and recommendations.

This project demonstrates how computer vision, applied statistics, and dashboard engineering can work together for real-world quality inspection workflows.

## Click-by-Click Recording Plan

1. Show the app title and sidebar.
2. Upload a sample image.
3. Pause on the summary metrics: Quality, Objects, Defect Rate, Resolution, Detector.
4. Open the Image tab and show original vs annotated image.
5. Open the Quality tab and show the quality gauge.
6. Open the Measurements tab and scroll across the measurement table.
7. Open the Inspection tab and show the issues or pass/review/fail result.
8. Open the SPC tab and show the control chart.
9. Open the Explainability tab and show the anomaly overlay.
10. Click the HTML report download button.

## Short LinkedIn Caption

I built VisionStat AI, a Streamlit-based computer vision and statistical quality inspection platform. It uploads images, assesses image quality, detects measurable regions, calculates object-level statistics, flags anomalies, creates SPC charts, and exports an inspection report. The default detector uses OpenCV contour analysis for reproducibility, with optional YOLO support for deep-learning detection.

## 15 Second Portfolio Pitch

VisionStat AI is a computer vision quality inspection dashboard. It converts uploaded images into measurable data, calculates quality and object statistics, flags anomalies, generates SPC charts, and exports a professional inspection report.
