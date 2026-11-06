
import gradio as gr
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# =====================================
# 1. LOAD TRAINED CNN MODEL
# =====================================

MODEL_PATH = r"E:\full stack data science\deep learning\CNN\Emotion Detection\emotion_model.keras"

model = load_model(MODEL_PATH)

print("Model loaded successfully!")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)


# =====================================
# 2. CLASS MAPPING
# =====================================

# Change this mapping according to:
# print(train_dataset.class_indices)

CLASS_INDICES = {
    "Happy": 0,
    "Sad": 1
}

# Output index -> emotion name
INDEX_TO_CLASS = {
    index: name
    for name, index in CLASS_INDICES.items()
}


# =====================================
# 3. FACE DETECTION
# =====================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

if face_cascade.empty():
    raise RuntimeError("Face detector could not be loaded!")


# =====================================
# 4. EMOTION PREDICTION
# =====================================

def predict_emotion(image):

    if image is None:
        return None, "Please upload an image."

    # Gradio image is RGB
    image = np.array(image).copy()

    # Convert RGB to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    # Detect face
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    if len(faces) == 0:
        return image, "No face detected!"

    predictions = []

    for (x, y, w, h) in faces:

        # Crop face
        face = image[y:y+h, x:x+w]

        # Resize
        face = cv2.resize(
            face,
            (200, 200)
        )

        # Normalize
        face = face.astype("float32") / 255.0

        # Add batch dimension
        face = np.expand_dims(face, axis=0)

        # CNN prediction
        pred = float(
            model.predict(face, verbose=0)[0][0]
        )

        # Sigmoid output represents class index 1
        probabilities = {
            0: 1 - pred,
            1: pred
        }

        predicted_index = max(
            probabilities,
            key=probabilities.get
        )

        emotion = INDEX_TO_CLASS[predicted_index]

        confidence = (
            probabilities[predicted_index] * 100
        )

        predictions.append(
            f"{emotion}: {confidence:.2f}%"
        )

        # Rectangle color
        if emotion == "Happy":
            color = (0, 200, 0)
        else:
            color = (255, 0, 0)

        # Draw rectangle
        cv2.rectangle(
            image,
            (x, y),
            (x+w, y+h),
            color,
            3
        )

        # Display prediction
        label = f"{emotion}: {confidence:.2f}%"

        cv2.putText(
            image,
            label,
            (x, max(y-10, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    result = "\n".join(predictions)

    return image, result


# =====================================
# 5. GRADIO INTERFACE
# =====================================

with gr.Blocks(title="CNN Emotion Detection") as demo:

    gr.Markdown(
        """
        # 😊 CNN Emotion Detection

        Upload your face image to predict Happy or Sad emotion.
        """
    )

    with gr.Row():

        input_image = gr.Image(
            type="numpy",
            label="Upload Image"
        )

        output_image = gr.Image(
            label="Prediction Result"
        )

    output_text = gr.Textbox(
        label="Detected Emotion"
    )

    predict_btn = gr.Button(
        "Predict Emotion",
        variant="primary"
    )

    predict_btn.click(
        fn=predict_emotion,
        inputs=input_image,
        outputs=[
            output_image,
            output_text
        ]
    )


# =====================================
# 6. LAUNCH APP
# =====================================

demo.launch(
    share=True
)
