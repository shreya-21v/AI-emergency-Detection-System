import cv2
from mtcnn import MTCNN

detector = MTCNN()
cap = cv2.VideoCapture(0)

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

            # Prevent negative coordinates
            x, y = max(0, x), max(0, y)

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # ---- FACE CROP ----
            h_frame, w_frame, _ = frame.shape
            x_end = min(x + w, w_frame)
            y_end = min(y + h, h_frame)
            face_crop = frame[y:y_end, x:x_end]

            # Resize for model input (Teachable Machine default)
            face_crop = cv2.resize(face_crop, (224, 224))

            # Show cropped face
            cv2.imshow("Face Crop", face_crop)

    cv2.imshow("Face Detection - MTCNN", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
