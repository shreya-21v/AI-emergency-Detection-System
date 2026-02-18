import cv2
from face_module import get_face_distress_score
from fusion_engine import FusionEngine
from voice_module import get_voice_distress_score
from emergency_module import send_sos
from gesture_module import detect_gesture
import time

fusion = FusionEngine()
cap = cv2.VideoCapture(0)
sos_sent = False
gesture_start_time = None
GESTURE_CONFIRM_TIME = 3   # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    face_score = get_face_distress_score(frame)
    voice_distress_score = get_voice_distress_score()
    gesture_detected = detect_gesture(frame)

    emergency = fusion.update(face_score, voice_distress_score)

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

    cv2.putText(frame, f"Face Score: {int(face_score)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Voice Score: {int(voice_distress_score)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    if gesture_detected:
        cv2.putText(frame, "OPEN PALM DETECTED", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    if emergency:
        cv2.putText(frame, "EMERGENCY DETECTED", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    if emergency and not sos_sent:
        print("EMERGENCY TRIGGERED")
        send_sos()
        sos_sent = True

    cv2.imshow("Emergency Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



