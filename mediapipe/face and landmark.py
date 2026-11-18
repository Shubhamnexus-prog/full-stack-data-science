
import cv2
import time
import mediapipe as mp

# Initialize MediaPipe Holistic
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic_model = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    refine_face_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Open webcam
capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("Error: Webcam not detected!")
    holistic_model.close()
    raise SystemExit

previous_time = 0

try:
    while capture.isOpened():

        ret, frame = capture.read()

        if not ret:
            print("Unable to read webcam frame.")
            break

        # Resize frame
        frame = cv2.resize(frame, (800, 600))

        # Convert BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # MediaPipe prediction
        results = holistic_model.process(image)

        image.flags.writeable = True

        # Convert RGB back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw face landmarks
        if results.face_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.face_landmarks,
                mp_holistic.FACEMESH_CONTOURS,
                mp_drawing.DrawingSpec(
                    color=(255, 0, 255),
                    thickness=1,
                    circle_radius=1
                ),
                mp_drawing.DrawingSpec(
                    color=(0, 255, 255),
                    thickness=1,
                    circle_radius=1
                )
            )

        # Draw pose landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS
            )

        # Draw right hand
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS
            )

        # Draw left hand
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS
            )

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time) if previous_time else 0
        previous_time = current_time

        cv2.putText(
            image,
            f"FPS: {int(fps)}",
            (10, 40),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display webcam output
        cv2.imshow("MediaPipe Holistic Detection", image)

        # Press ESC to exit
        if cv2.waitKey(5) & 0xFF == 27:
            break

finally:
    capture.release()
    holistic_model.close()
    cv2.destroyAllWindows()

print("Holistic detection stopped.")
