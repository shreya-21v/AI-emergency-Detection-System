import streamlit as st
import json
import time
import os
from PIL import Image

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Emergency Dashboard",
    layout="wide",
    page_icon="🚨"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main-title {
    font-size: 40px;
    font-weight: 700;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.metric-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}

.metric-title {
    font-size: 18px;
    color: #aaa;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: white;
}

.normal-box {
    background-color: #1f3d2b;
    color: #00ff88;
    padding: 20px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
}

.emergency-box {
    background-color: #4d0000;
    color: #ff4d4d;
    padding: 20px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0.5; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.markdown('<div class="main-title">🚨 AI Emergency Detection Dashboard</div>', unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #
data = {
    "face_score": 0,
    "voice_score": 0,
    "gesture": False,
    "emergency": False
}

if os.path.exists("dashboard_data.json"):
    try:
        with open("dashboard_data.json", "r") as f:
            data = json.load(f)
    except:
        pass

# ---------------- METRICS ---------------- #
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Face Score</div>
        <div class="metric-value">{round(data["face_score"],2)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Voice Score</div>
        <div class="metric-value">{round(data["voice_score"],2)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Gesture</div>
        <div class="metric-value">{'YES' if data["gesture"] else 'NO'}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if data["emergency"]:
        st.markdown("""
        <div class="emergency-box">
            🚨 EMERGENCY DETECTED
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="normal-box">
            ✅ SYSTEM NORMAL
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- CAMERA FEED ---------------- #
st.subheader("📷 Live Camera Feed")

if os.path.exists("dashboard_frame.jpg"):
    try:
        img = Image.open("dashboard_frame.jpg")
        st.image(img, use_container_width=700)
    except:
        st.warning("Camera frame loading...")
else:
    st.warning("Waiting for camera feed...")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- LOCATION ---------------- #
st.subheader("📍 Current Location")

if os.path.exists("location_data.json"):
    try:
        with open("location_data.json", "r") as f:
            location = json.load(f)
        st.success(f"Latitude: {location['latitude']} | Longitude: {location['longitude']}")
    except:
        st.info("Location not available.")
else:
    st.info("Location not available.")

# ---------------- AUTO REFRESH ---------------- #
time.sleep(1)
st.rerun()
