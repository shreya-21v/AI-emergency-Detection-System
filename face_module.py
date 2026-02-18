import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from collections import deque

detector = MTCNN()
model = load_model("keras_model.h5", compile=False)

score_buffer = deque(maxlen=10)

def get_face_distress_score(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        faces = detector.detect_faces(rgb_frame)
    except:
        faces = []

    if faces:
        x, y, w, h = faces[0]['box']
        x, y = max(0, x), max(0, y)

        face_crop = frame[y:y+h, x:x+w]
        face_crop = cv2.resize(face_crop, (224, 224))

        img = face_crop.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img, verbose=0)
        distress_prob = prediction[0][0] * 100

        score_buffer.append(distress_prob)
        return sum(score_buffer) / len(score_buffer)

    return 0
