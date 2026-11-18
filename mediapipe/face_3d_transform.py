
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe initialization
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

drawing_spec = mp_drawing.DrawingSpec(
    thickness=1,
    circle_radius=1,
    color=(0, 255, 0)
)

# Webcam initialization
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

# Capture replacement face
print("Look at the camera to capture your replacement face.")

ret, replacement_face = cap.read()

if not ret:
    cap.release()
    face_mesh.close()
    raise RuntimeError("Failed to capture replacement face")

replacement_face = cv2.flip(replacement_face, 1)

# Detect face in replacement image
replacement_rgb = cv2.cvtColor(
    replacement_face, cv2.COLOR_BGR2RGB
)

replacement_results = face_mesh.process(replacement_rgb)

if not replacement_results.multi_face_landmarks:
    cap.release()
    face_mesh.close()
    raise RuntimeError("No face detected in replacement image")

print("Replacement face captured successfully!")


def get_face_bbox(face_landmarks, image_shape):

    height, width = image_shape[:2]

    x_values = [
        landmark.x for landmark in face_landmarks.landmark
    ]

    y_values = [
        landmark.y for landmark in face_landmarks.landmark
    ]

    xmin = max(0, int(min(x_values) * width))
    ymin = max(0, int(min(y_values) * height))

    xmax = min(width, int(max(x_values) * width))
    ymax = min(height, int(max(y_values) * height))

    return xmin, ymin, xmax, ymax


def transform_face(image, landmarks, replacement):

    output = image.copy()

    xmin, ymin, xmax, ymax = get_face_bbox(
        landmarks, image.shape
    )

    if xmax <= xmin or ymax <= ymin:
        return output

    face_width = xmax - xmin
    face_height = ymax - ymin

    replacement_resized = cv2.resize(
        replacement,
        (face_width, face_height)
    )

    # Soft elliptical mask
    mask = np.zeros(
        (face_height, face_width),
        dtype=np.float32
    )

    center = (face_width // 2, face_height // 2)

    axes = (
        max(1, int(face_width * 0.45)),
        max(1, int(face_height * 0.47))
    )

    cv2.ellipse(
        mask,
        center,
        axes,
        0,
        0,
        360,
        1.0,
        -1
    )

    mask = cv2.GaussianBlur(mask, (21, 21), 0)

    # Blend replacement face with original frame
    roi = output[ymin:ymax, xmin:xmax]

    blended = (
        replacement_resized.astype(np.float32)
        * mask[:, :, np.newaxis]
        +
        roi.astype(np.float32)
        * (1 - mask[:, :, np.newaxis])
    )

    output[ymin:ymax, xmin:xmax] = np.clip(
        blended, 0, 255
    ).astype(np.uint8)

    return output


try:

    while cap.isOpened():

        success, image = cap.read()

        if not success:
            break

        image = cv2.flip(image, 1)

        image_rgb = cv2.cvtColor(
            image, cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(image_rgb)

        transformed_image = image.copy()

        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:

                transformed_image = transform_face(
                    image,
                    face_landmarks,
                    replacement_face
                )

                # Draw face mesh
                mp_drawing.draw_landmarks(
                    transformed_image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec
                )

        # Resize replacement image for display
        left_image = cv2.resize(
            replacement_face, (400, 400)
        )

        right_image = cv2.resize(
            transformed_image, (400, 400)
        )

        composite = np.hstack(
            (left_image, right_image)
        )

        cv2.putText(
            composite,
            "Replacement Face",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            composite,
            "Transformed Output",
            (410, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "MediaPipe Face Transformation",
            composite
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:

    cap.release()
    face_mesh.close()
    cv2.destroyAllWindows()

print("Face transformation stopped.")
