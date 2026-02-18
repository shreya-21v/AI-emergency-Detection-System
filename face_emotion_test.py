import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from collections import deque

# Load model
model = load_model("keras_model.h5", compile=False)

detector = MTCNN()
cap = cv2.VideoCapture(0)

# ---- SMOOTHING BUFFER ----
score_buffer = deque(maxlen=10)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        faces = detector.detect_faces(rgb_frame)
    except:
        faces = []

    if faces:
        for face in faces:
            x, y, w, h = face['box']
            x, y = max(0, x), max(0, y)

            face_crop = frame[y:y+h, x:x+w]
            face_crop = cv2.resize(face_crop, (224, 224))

            img = face_crop.astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=0)

            prediction = model.predict(img, verbose=0)

            distress_prob = prediction[0][0] * 100

            # ---- ADD TO BUFFER ----
            score_buffer.append(distress_prob)

            # ---- SMOOTHED SCORE ----
            face_distress_score = sum(score_buffer) / len(score_buffer)

            cv2.putText(
                frame,
                f"Distress: {int(face_distress_score)}%",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Distress Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
