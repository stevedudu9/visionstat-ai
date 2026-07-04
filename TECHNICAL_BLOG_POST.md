# Building VisionStat AI: Computer Vision Meets Statistical Quality Control

## Introduction

VisionStat AI is a computer vision analytics and statistical quality inspection platform. The project is designed around a practical question: how can an image become measurable evidence for quality decisions?

Instead of stopping at image classification, the application extracts measurements, evaluates image quality, identifies unusual regions, creates statistical process control charts, and generates an inspection report.

The app is built with Streamlit, OpenCV, NumPy, Pandas, and Plotly.

## Why This Project Matters

Many inspection workflows depend on visual judgment. A person may look at an image and decide whether a product, sample, or object looks acceptable. That process can be subjective, inconsistent, and hard to audit.

VisionStat AI turns visual data into structured measurements. Once the image is converted into data, statistical methods can be applied:

- Is the image good enough for inspection?
- How many measurable regions were detected?
- Are any regions unusually large, small, or irregular?
- Are color patterns inconsistent?
- Is the process stable?
- Should the result pass, fail, or require review?

## Current Detection Method

By default, VisionStat AI uses OpenCV contour-based detection. This makes the project lightweight, reproducible, and easy to deploy without requiring a trained deep learning model.

The contour workflow is:

1. Convert the image to grayscale.
2. Apply Gaussian blur to reduce noise.
3. Use Canny edge detection to find boundaries.
4. Use morphological closing to connect nearby edges.
5. Extract external contours.
6. Filter very small regions.
7. Convert each contour into a bounding box and measurement record.

This method detects measurable regions, not semantic object classes. If a compatible YOLO model is provided, the app can optionally perform deep-learning-based object detection.

## Image Quality Assessment

Before trusting measurement results, the app evaluates whether the image itself is suitable for inspection.

The quality module calculates:

- Brightness: average grayscale intensity
- Contrast: standard deviation of grayscale intensity
- Sharpness: variance of the Laplacian response
- Blur index: inverse indicator derived from sharpness
- Noise estimate: residual variation after median filtering
- Resolution: megapixels from image width and height

Each metric is converted into a score, then combined into a weighted image quality score.

This matters because poor lighting, blur, low contrast, or low resolution can make downstream detection unreliable.

## Statistical Measurements

For each detected region, VisionStat AI calculates:

- X and Y position
- Width and height
- Area in pixels
- Perimeter
- Aspect ratio
- Circularity
- Mean red, green, and blue values
- Detection confidence

These measurements turn visual regions into tabular data. Once the data is tabular, it can be summarized, visualized, compared, and audited.

## Quality Inspection Logic

The app produces a Pass, Review, or Fail decision.

The decision considers:

- Overall image quality score
- Whether measurable objects were detected
- Size deviation based on area z-scores
- Color inconsistency across detected regions
- Estimated defect rate

This is intentionally transparent. The goal is not to hide decisions inside a black-box model, but to provide explainable inspection rules that can be improved over time.

## Anomaly Scoring

Anomaly scoring is based on standardized feature differences. The app compares each detected region against the average region using features such as:

- Area
- Aspect ratio
- Circularity
- Mean red
- Mean green
- Mean blue

For each object, the app calculates the average absolute standardized deviation. Higher values indicate that the region differs more strongly from the rest of the detected objects.

This method is simple, explainable, and useful for prototype inspection workflows.

## Statistical Process Control

The SPC module creates a control chart for a selected metric such as area, width, height, aspect ratio, or circularity.

The chart includes:

- Center line: process mean
- Upper control limit: mean plus three standard deviations
- Lower control limit: mean minus three standard deviations
- Warning limits: mean plus or minus two standard deviations
- Out-of-control indicator

The app also estimates process capability using Cp and Cpk. These metrics compare process variation against specification limits. In this prototype, specification limits are estimated around the observed mean, so they should be replaced with real engineering tolerances in production.

## Explainability

VisionStat AI includes explainability in two ways:

1. It shows tabular confidence and anomaly scores.
2. It creates a visual anomaly and edge-response overlay.

This helps users understand where the app is focusing and why a result might require review.

## Report Generation

The app can export an HTML inspection report. The report includes:

- Image summary
- Quality score
- Inspection decision
- Detected object count
- Recommendations
- Inspection findings
- Process capability summary
- Measurement table

This makes the app useful beyond interactive exploration. Results can be saved, shared, or attached to project documentation.

## Limitations

The current prototype has important limits:

- OpenCV contour detection finds regions, not semantic classes.
- YOLO support requires the user to provide a compatible model.
- PDF export is not implemented yet; the current export is HTML.
- Quality thresholds are prototype defaults.
- Production use would require validation images, calibrated thresholds, model governance, and domain-specific acceptance criteria.

## Future Improvements

Useful next steps include:

- PDF export
- Sample image gallery
- Batch image upload
- Defect severity scoring
- YOLO model loading from cloud storage
- Segmentation support
- OCR integration
- Real-time camera inspection
- Calibration using known object dimensions
- User-defined specification limits for SPC

## Conclusion

VisionStat AI demonstrates how computer vision and statistics can work together in a practical quality inspection workflow. The project converts images into quantitative measurements, applies explainable statistical rules, visualizes process behavior, and generates a report.

It is a strong portfolio project because it connects AI, applied statistics, dashboard development, and real-world decision support.
