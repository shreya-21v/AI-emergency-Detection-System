import cv2
import time
import json
import os
from face_module import get_face_distress_score
from voice_module import get_voice_distress_score
from gesture_module import detect_gesture
from fusion_engine import FusionEngine
from emergency_module import send_sos
from location_module import get_location   # ✅ FIXED IMPORT

cap = cv2.VideoCapture(0)
fusion = FusionEngine()

gesture_start_time = None
GESTURE_CONFIRM_TIME = 3
sos_sent = False

# ✅ LOCATION VARIABLES (outside loop)
location_history = []
last_location_fetch = 0
LOCATION_REFRESH_INTERVAL = 10  # seconds

print("System running... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ---------------- FACE ----------------
    face_score = get_face_distress_score(frame)

    # ---------------- VOICE ----------------
    voice_score = get_voice_distress_score()

    # ---------------- GESTURE ----------------
    gesture_detected = detect_gesture(frame)

    # ---------------- FUSION ----------------
    emergency = fusion.update(face_score, voice_score)

    # ---------------- GESTURE TIMER ----------------
    if gesture_detected:
        if gesture_start_time is None:
            gesture_start_time = time.time()

        elapsed = time.time() - gesture_start_time

        cv2.putText(frame, f"Palm detected: {elapsed:.1f}s", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if elapsed > GESTURE_CONFIRM_TIME:
            emergency = True
    else:
        gesture_start_time = None

    # ---------------- GPS MODULE ----------------
    current_time = time.time()
    if current_time - last_location_fetch > LOCATION_REFRESH_INTERVAL:
        lat, lon = get_location()
        last_location_fetch = current_time

        if lat and lon:
            location_history.append((lat, lon))

        if len(location_history) > 50:
            location_history.pop(0)

    # ---------------- DASHBOARD WRITE ----------------
    dashboard_data = {
        "face_score": float(face_score),
        "voice_score": float(voice_score),
        "gesture": bool(gesture_detected),
        "emergency": bool(emergency),
        "location_history": location_history  # ✅ now included
    }

    with open("dashboard_data.json", "w") as f:
        json.dump(dashboard_data, f)

    # Save frame for dashboard preview
    cv2.imwrite("temp_frame.jpg", frame)
    os.replace("temp_frame.jpg", "dashboard_frame.jpg")


    # ---------------- UI DISPLAY ----------------
    cv2.putText(frame, f"Face Score: {face_score:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Voice Score: {voice_score:.2f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    if gesture_detected:
        cv2.putText(frame, "Gesture: OPEN PALM", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    if emergency:
        cv2.putText(frame, "EMERGENCY DETECTED", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # ---------------- SOS TRIGGER ----------------
    if emergency and not sos_sent:
        print("EMERGENCY TRIGGERED")
        send_sos()
        sos_sent = True

    cv2.imshow("Emergency Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
