from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError

from visionstat.analysis import anomaly_scores, assess_quality, image_metadata, inspect_quality, measure_regions, pil_to_bgr
from visionstat.detection import annotate_image, detect_objects
from visionstat.reporting import build_html_report
from visionstat.spc import capability_metrics, control_chart_data
from visionstat.visualization import anomaly_heatmap, bgr_to_rgb, control_chart, measurement_distribution, quality_gauge


st.set_page_config(page_title="VisionStat AI", page_icon="VS", layout="wide")

st.markdown(
    """
    <style>
      .block-container { padding-top: 1.4rem; }
      [data-testid="stMetricValue"] { font-size: 1.8rem; }
      .status-pass { color: #166534; font-weight: 700; }
      .status-review { color: #92400e; font-weight: 700; }
      .status-fail { color: #991b1b; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)


def find_default_model() -> str | None:
    for candidate in ["yolov8n.pt", "yolo11n.pt", "model.pt", "best.pt"]:
        if Path(candidate).exists():
            return candidate
    return None


def main() -> None:
    st.title("VisionStat AI")
    st.caption("Computer vision analytics and statistical quality inspection")

    with st.sidebar:
        st.header("Inspection Setup")
        uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png", "bmp"])
        model_path = st.text_input("YOLO model path", value=find_default_model() or "")
        confidence = st.slider("Detection confidence", 0.05, 0.95, 0.25, 0.05)
        metric = st.selectbox("SPC metric", ["area_px", "width", "height", "aspect_ratio", "circularity"])

    if uploaded is None:
        render_empty_state()
        return

    try:
        image = Image.open(uploaded)
        image.verify()
        uploaded.seek(0)
        image = Image.open(uploaded)
    except (UnidentifiedImageError, OSError):
        st.error("The uploaded file could not be read as a valid image.")
        return

    bgr = pil_to_bgr(image)
    metadata = image_metadata(image, uploaded.name, uploaded.size)
    quality = assess_quality(bgr)
    detections, detector_name = detect_objects(bgr, model_path.strip() or None, confidence)
    measurements = measure_regions(bgr, detections)
    scored_measurements = anomaly_scores(measurements)
    inspection = inspect_quality(scored_measurements, quality)
    chart_data = control_chart_data(scored_measurements, metric)
    capability = capability_metrics(scored_measurements, metric)

    render_summary(metadata, quality, inspection, detections, detector_name)
    render_tabs(bgr, detections, quality, inspection, scored_measurements, chart_data, capability, metric)

    report_html = build_html_report(metadata, quality, inspection, detections, scored_measurements, capability)
    st.download_button(
        "Download HTML report",
        report_html,
        file_name=f"visionstat_report_{Path(uploaded.name).stem}.html",
        mime="text/html",
    )


def render_empty_state() -> None:
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Upload an inspection image to begin")
        st.write("The dashboard will calculate image quality, detect measurable regions, flag anomalies, build SPC charts, and generate a downloadable inspection report.")
    with right:
        st.info("Supported formats: JPG, JPEG, PNG, BMP")


def render_summary(metadata, quality, inspection, detections, detector_name: str) -> None:
    status_class = {
        "Pass": "status-pass",
        "Review": "status-review",
        "Fail": "status-fail",
    }.get(inspection["decision"], "status-review")
    st.markdown(f"### Decision: <span class='{status_class}'>{inspection['decision']}</span>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Quality", f"{quality['quality_score']:.1f}/100")
    c2.metric("Objects", len(detections))
    c3.metric("Defect rate", f"{inspection['defect_rate']:.1f}%")
    c4.metric("Resolution", f"{quality['resolution_mp']:.2f} MP")
    c5.metric("Detector", detector_name)

    with st.expander("Image properties", expanded=False):
        st.dataframe(pd.DataFrame([metadata.__dict__]), use_container_width=True)


def render_tabs(bgr, detections, quality, inspection, measurements, chart_data, capability, metric: str) -> None:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Image", "Quality", "Measurements", "Inspection", "SPC", "Explainability"]
    )

    with tab1:
        left, right = st.columns(2)
        left.image(bgr_to_rgb(bgr), caption="Original image", use_container_width=True)
        right.image(bgr_to_rgb(annotate_image(bgr, detections)), caption="Annotated detections", use_container_width=True)

    with tab2:
        left, right = st.columns([1, 1.2])
        left.plotly_chart(quality_gauge(quality["quality_score"]), use_container_width=True)
        quality_table = pd.DataFrame(
            [
                {"metric": "Brightness", "value": round(quality["brightness"], 2)},
                {"metric": "Contrast", "value": round(quality["contrast"], 2)},
                {"metric": "Sharpness", "value": round(quality["sharpness"], 2)},
                {"metric": "Blur index", "value": round(quality["blur_index"], 2)},
                {"metric": "Noise", "value": round(quality["noise"], 2)},
            ]
        )
        right.dataframe(quality_table, use_container_width=True, hide_index=True)
        for item in quality["recommendations"]:
            st.write(f"- {item}")

    with tab3:
        if measurements.empty:
            st.warning("No measurable regions were found.")
        else:
            st.dataframe(measurements, use_container_width=True, hide_index=True)
            st.plotly_chart(measurement_distribution(measurements, metric), use_container_width=True)

    with tab4:
        for item in inspection["issues"]:
            st.write(f"- {item}")
        if not measurements.empty:
            flagged = measurements.loc[measurements.get("anomaly_flag", False) == True]
            if not flagged.empty:
                st.dataframe(flagged, use_container_width=True, hide_index=True)

    with tab5:
        if chart_data.empty:
            st.warning("SPC needs at least one detected measurement.")
        else:
            st.plotly_chart(control_chart(chart_data, metric), use_container_width=True)
            if capability.get("status") == "Insufficient data":
                st.info("Process capability needs at least two measurements.")
            st.json(capability)

    with tab6:
        st.image(bgr_to_rgb(anomaly_heatmap(bgr)), caption="Anomaly and edge-response overlay", use_container_width=True)
        if not measurements.empty:
            confidence_summary = measurements[["id", "label", "confidence", "anomaly_score", "anomaly_flag"]]
            st.dataframe(confidence_summary, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
