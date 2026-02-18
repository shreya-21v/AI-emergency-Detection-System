import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)

def is_open_palm(hand_landmarks):
    # finger tip landmarks
    tips = [8, 12, 16, 20]

    # finger base landmarks
    bases = [6, 10, 14, 18]

    extended = 0

    for tip, base in zip(tips, bases):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
            extended += 1

    return extended >= 3   # at least 3 fingers extended

def detect_gesture(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            if is_open_palm(hand_landmarks):
                return True

    return False
