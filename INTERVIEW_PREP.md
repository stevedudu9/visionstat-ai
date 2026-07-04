# VisionStat AI Interview Prep

## One-Minute Project Explanation

VisionStat AI is a Streamlit dashboard that combines computer vision with statistical quality control. A user uploads an image, and the app evaluates image quality, detects measurable regions, calculates object measurements, flags anomalies, creates SPC charts, and generates an HTML inspection report.

The default detector uses OpenCV contour analysis so the app is lightweight and reproducible. If a user provides a YOLO model, the app can optionally perform deep-learning-based object detection.

The project demonstrates computer vision, feature extraction, applied statistics, dashboard engineering, and explainable quality inspection.

## Thirty-Second Version

VisionStat AI turns uploaded images into measurable inspection data. It checks image quality, detects regions, measures object properties, flags anomalies, creates control charts, and exports a report. I built it to show how computer vision and statistics can support quality assurance decisions.

## Technical Questions And Strong Answers

### Why did you use OpenCV contour detection by default?

I wanted the default version to be lightweight, reproducible, and easy to deploy. Contour detection does not require a trained model or large model file, so anyone can run the app immediately. I also added optional YOLO support for cases where semantic object detection is needed.

### What is the limitation of contour detection?

Contour detection finds measurable regions based on edges and shapes, but it does not understand object categories. It can detect a region, measure it, and flag irregularity, but it cannot reliably label that region as a specific object unless a semantic model like YOLO is used.

### How is the image quality score calculated?

The app calculates brightness, contrast, sharpness, blur, noise, and resolution. Each metric is converted into a score, then combined with weights into an overall quality score. The purpose is to estimate whether the image is reliable enough for automated inspection.

### How do you detect blur?

I use the variance of the Laplacian. A sharp image usually has stronger edge variation, while a blurry image has weaker high-frequency detail. Lower Laplacian variance suggests more blur.

### How do you estimate noise?

The app applies a median filter and compares the filtered image to the original grayscale image. The residual variation gives a simple estimate of noise.

### What measurements do you extract?

For each detected region, the app extracts area, width, height, perimeter, aspect ratio, circularity, mean RGB color values, position, and confidence.

### How does anomaly detection work?

The app standardizes object-level features and calculates the average absolute deviation for each detected region. Regions that differ strongly from the others receive higher anomaly scores.

### What statistical process control method did you implement?

I implemented a control chart with a center line, upper and lower control limits at plus or minus three standard deviations, and warning limits at plus or minus two standard deviations. The app also estimates Cp and Cpk for process capability.

### What does Cpk mean?

Cpk measures how well a process fits within specification limits while accounting for whether the process mean is centered. A higher Cpk means the process has less risk of producing outputs outside specifications.

### Are the Cp and Cpk values production-ready?

Not yet. In this prototype, specification limits are estimated around the observed mean. In production, those limits should come from engineering tolerances or quality requirements.

### How does the app decide Pass, Review, or Fail?

The decision combines image quality, object detection success, size deviation, color inconsistency, and defect rate. It is rule-based and explainable, so users can understand why the app recommends review or failure.

### Why is explainability important here?

Quality inspection decisions need trust and auditability. The app shows the measurements, anomaly scores, confidence values, and visual overlays so users can inspect the reasoning instead of only seeing a final label.

### What would you improve next?

I would add batch upload, PDF export, user-defined SPC specification limits, calibrated thresholds, sample datasets, and trained YOLO or segmentation models for domain-specific inspection.

## Behavioral Interview Framing

### Challenge

I wanted to build a project that was more than a simple image classifier. The challenge was integrating computer vision, statistical quality control, visualization, and reporting into one usable app.

### Action

I split the system into modules: image quality, detection, measurement, inspection, anomaly scoring, SPC, visualization, and reporting. I used OpenCV for reproducible image processing and Streamlit for the interactive dashboard.

### Result

The final app can upload images, produce quality metrics, detect regions, generate object measurements, flag anomalies, visualize SPC charts, and export an inspection report. It is also documented and includes a self-test for verification.

## Questions To Ask Interviewers

- How does your team validate computer vision models before production?
- Do you use statistical process control in your quality workflows?
- What kinds of image defects or anomalies are most important in your domain?
- How do you balance model accuracy with explainability?
- What deployment environment do your analytics dashboards usually use?

## Portfolio Talking Points

- Built a full computer vision analytics workflow, not just a model demo.
- Combined OpenCV image processing with statistical quality control.
- Designed the app for explainability and reproducibility.
- Added optional YOLO support without making it required.
- Included audit documentation and a self-test script.
- Identified honest limitations and realistic production improvements.
