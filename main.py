import cv2
import time
import json

from face_module import get_face_distress_score
from voice_module import get_voice_distress_score
from gesture_module import detect_gesture
from fusion_engine import FusionEngine
from emergency_module import send_sos

cap = cv2.VideoCapture(0)
fusion = FusionEngine()

gesture_start_time = None
GESTURE_CONFIRM_TIME = 3  # seconds
sos_sent = False

print("System running... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FACE MODULE
    face_score = get_face_distress_score(frame)

    # VOICE MODULE
    voice_score = get_voice_distress_score()

    # GESTURE MODULE
    gesture_detected = detect_gesture(frame)

    # FUSION ENGINE
    emergency = fusion.update(face_score, voice_score)

    # GESTURE CONFIRMATION TIMER
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

    # DASHBOARD DATA WRITE
    dashboard_data = {
        "face_score": float(face_score),
        "voice_score": float(voice_score),
        "gesture": bool(gesture_detected),
        "emergency": bool(emergency)
    }

    with open("dashboard_data.json", "w") as f:
        json.dump(dashboard_data, f)

    # SAVE CAMERA FRAME FOR DASHBOARD
    cv2.imwrite("dashboard_frame.jpg", frame)

    # UI TEXT
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

    # SEND SOS ONLY ONCE
    if emergency and not sos_sent:
        print("EMERGENCY TRIGGERED")
        send_sos()
        sos_sent = True

    cv2.imshow("Emergency Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
