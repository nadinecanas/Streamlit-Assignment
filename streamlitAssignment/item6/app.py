# realtime_cv_app.py
import streamlit as st
import cv2
import numpy as np
from datetime import datetime

st.title("📹 Real-Time Video Stream with OpenCV")
st.write("This app captures live video from your webcam, applies real-time filters, and allows snapshots!")

# Sidebar controls
st.sidebar.header("⚙️ Filter Controls")
low_threshold = st.sidebar.slider('Canny Low Threshold', 0, 255, 100)
high_threshold = st.sidebar.slider('Canny High Threshold', 0, 255, 200)

# Checkbox to enable/disable filter
apply_filter = st.sidebar.checkbox("Apply Canny Edge Filter", value=True)

# Button for snapshot
snapshot_btn = st.sidebar.button("📸 Take Snapshot")

# Streamlit placeholder for image
frame_placeholder = st.empty()

# Capture video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("❌ Cannot access webcam. Please check permissions or hardware.")
else:
    run = st.checkbox("Start Video", value=True)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Failed to grab frame.")
            break

        # Flip horizontally for mirror effect
        frame = cv2.flip(frame, 1)

        # Apply filter if checked
        if apply_filter:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, low_threshold, high_threshold)
            frame_display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        else:
            frame_display = frame

        # Convert BGR to RGB
        frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)

        # Display image
        frame_placeholder.image(frame_display, channels="RGB")

        # Snapshot
        if snapshot_btn:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.png"
            cv2.imwrite(filename, cv2.cvtColor(frame_display, cv2.COLOR_RGB2BGR))
            st.success(f"📸 Snapshot saved as {filename}")

    cap.release()

