
# -------------- IMPORT LIBRARIES --------------

import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt

# -------------- MEDIAPIPE OBJECTRON --------------

mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

# -------------- LOAD IMAGE --------------

image_path = "mug.jpg"

mug = cv2.imread(image_path)

if mug is None:
    raise FileNotFoundError(
        f"Image not found or could not be loaded: {image_path}"
    )

# Convert BGR to RGB
mug = cv2.cvtColor(mug, cv2.COLOR_BGR2RGB)

# -------------- CREATE OBJECTRON MODEL --------------

with mp_objectron.Objectron(
    static_image_mode=True,
    max_num_objects=5,
    min_detection_confidence=0.2,
    model_name="Cup"
) as objectron:

    # Run inference
    results = objectron.process(mug)

# -------------- DISPLAY DETECTION --------------

annotated_image = mug.copy()

if not results.detected_objects:
    print("No 3D box landmarks detected.")

else:
    print(f"Detected objects: {len(results.detected_objects)}")

    for detected_object in results.detected_objects:

        # Draw 3D bounding box landmarks
        mp_drawing.draw_landmarks(
            annotated_image,
            detected_object.landmarks_2d,
            mp_objectron.BOX_CONNECTIONS
        )

        # Draw 3D coordinate axis
        mp_drawing.draw_axis(
            annotated_image,
            detected_object.rotation,
            detected_object.translation
        )

# -------------- DISPLAY RESULT --------------

plt.figure(figsize=(10, 10))
plt.imshow(annotated_image)
plt.axis("off")
plt.title("MediaPipe 3D Object Detection")
plt.show()
