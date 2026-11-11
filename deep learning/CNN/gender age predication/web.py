
import os
import cv2
import time
import numpy as np

from tensorflow.keras.models import load_model


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "age_gender_cnn.keras"
)

IMAGE_SIZE = 64
CHANNELS = 1

GENDER_LABELS = {
    0: "Male",
    1: "Female"
}


# ==========================================
# 2. LOAD CUSTOM CNN MODEL
# ==========================================

print("Loading CNN model...")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

model = load_model(MODEL_PATH)

print("CNN model loaded successfully!")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)


# ==========================================
# 3. LOAD OPENCV FACE DETECTOR
# ==========================================

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)

if face_detector.empty():
    raise RuntimeError("Haar Cascade loading failed!")

print("Face detector loaded successfully!")


# ==========================================
# 4. PREPROCESS FACE
# ==========================================

def preprocess_face(face):

    face = cv2.resize(
        face,
        (IMAGE_SIZE, IMAGE_SIZE)
    )

    face = face.astype(np.float32) / 255.0

    face = face.reshape(
        IMAGE_SIZE,
        IMAGE_SIZE,
        CHANNELS
    )

    return face


# ==========================================
# 5. REAL-TIME WEBCAM APPLICATION
# ==========================================

def start_webcam():

    # Open default webcam
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()

        # Fallback for systems where CAP_DSHOW fails
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Webcam could not be opened!")
        print("Check camera connection and permissions.")
        return

    # Camera settings
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("\nWebcam started successfully!")
    print("Press Q to quit.")
    print("Press S to save screenshot.")

    frame_count = 0

    # FPS calculation
    previous_time = time.time()

    try:

        while True:

            # Read camera frame
            ret, frame = camera.read()

            if not ret:
                print("Unable to read webcam frame.")
                break

            frame_count += 1

            # Flip horizontally like a mirror
            frame = cv2.flip(frame, 1)

            # Convert to grayscale
            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            # Face detection
            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60)
            )

            face_batch = []

            # ==================================
            # 6. EXTRACT ALL DETECTED FACES
            # ==================================

            for (x, y, w, h) in faces:

                face = gray[y:y+h, x:x+w]

                processed_face = preprocess_face(face)

                face_batch.append(processed_face)

            # ==================================
            # 7. BATCH CNN PREDICTION
            # ==================================

            if len(face_batch) > 0:

                face_batch = np.array(
                    face_batch,
                    dtype=np.float32
                )

                age_outputs, gender_outputs = model.predict(
                    face_batch,
                    verbose=0
                )

                # ==================================
                # 8. DISPLAY PREDICTIONS
                # ==================================

                for i, (x, y, w, h) in enumerate(faces):

                    age = float(age_outputs[i][0])

                    age = float(np.clip(age, 0, 116))

                    gender_probability = float(
                        gender_outputs[i][0]
                    )

                    gender_class = (
                        1 if gender_probability >= 0.5 else 0
                    )

                    gender = GENDER_LABELS[gender_class]

                    gender_score = (
                        gender_probability
                        if gender_class == 1
                        else 1 - gender_probability
                    )

                    label = (
                        f"Age: {age:.1f} | {gender}"
                    )

                    # Draw face rectangle
                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        2
                    )

                    # Label background
                    label_y = max(y - 35, 0)

                    cv2.rectangle(
                        frame,
                        (x, label_y),
                        (x+w, y),
                        (0, 255, 0),
                        -1
                    )

                    # Display prediction
                    cv2.putText(
                        frame,
                        label,
                        (x+5, max(y-10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 0, 0),
                        2
                    )

                    # Gender score below face
                    cv2.putText(
                        frame,
                        f"Model score: {gender_score*100:.1f}%",
                        (x, y+h+22),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        1
                    )

            # ==================================
            # 9. DISPLAY FPS AND FACE COUNT
            # ==================================

            current_time = time.time()

            fps = 1.0 / max(
                current_time - previous_time,
                0.000001
            )

            previous_time = current_time

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Faces: {len(faces)}",
                (15, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Press Q: Quit | S: Screenshot",
                (15, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            # Show webcam
            cv2.imshow(
                "Real-Time Age and Gender Prediction",
                frame
            )

            # ==================================
            # 10. KEYBOARD CONTROLS
            # ==================================

            key = cv2.waitKey(1) & 0xFF

            # Quit
            if key == ord("q"):
                print("Closing webcam...")
                break

            # Save screenshot
            elif key == ord("s"):

                screenshot_path = os.path.join(
                    BASE_DIR,
                    f"webcam_capture_{frame_count}.jpg"
                )

                cv2.imwrite(
                    screenshot_path,
                    frame
                )

                print(
                    "Screenshot saved:",
                    screenshot_path
                )

    finally:

        # Release resources
        camera.release()

        cv2.destroyAllWindows()

        print("Webcam closed successfully!")


# ==========================================
# 11. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("\n====================================")
    print("REAL-TIME AGE AND GENDER PREDICTION")
    print("====================================")

    start_webcam()
