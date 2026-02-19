import streamlit as st
import json
import time
import os
from PIL import Image

st.set_page_config(page_title="AI Emergency Dashboard", layout="wide")

st.title("AI Emergency Detection Dashboard")

placeholder = st.empty()

while True:
    with placeholder.container():

        col1, col2, col3 = st.columns(3)

        # READ DASHBOARD DATA
        if os.path.exists("dashboard_data.json"):
            with open("dashboard_data.json", "r") as f:
                data = json.load(f)

            face_score = data["face_score"]
            voice_score = data["voice_score"]
            gesture = data["gesture"]
            emergency = data["emergency"]

        else:
            face_score = 0
            voice_score = 0
            gesture = False
            emergency = False

        col1.metric("Face Score", f"{face_score:.2f}")
        col2.metric("Voice Score", f"{voice_score:.2f}")
        col3.metric("Gesture", "YES" if gesture else "NO")

        st.divider()

        # CAMERA PREVIEW
        if os.path.exists("dashboard_frame.jpg"):
            img = Image.open("dashboard_frame.jpg")
            st.image(img, caption="Live Camera Feed")
        else:
            st.warning("Waiting for camera feed...")

        st.divider()

        # STATUS BOX
        if emergency:
            st.error("EMERGENCY DETECTED")
        else:
            st.success("SYSTEM NORMAL")

    time.sleep(1)
