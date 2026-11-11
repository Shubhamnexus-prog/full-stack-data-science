
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Age & Gender Prediction",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Age & Gender Prediction")
st.write("CNN-based facial age estimation and gender-label prediction")

# --------------------------------------------------
# 2. MODEL CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "age_gender_cnn.keras"

IMAGE_SIZE = 64

# --------------------------------------------------
# 3. LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_prediction_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return load_model(MODEL_PATH, compile=False)


try:
    model = load_prediction_model()
    st.success("CNN model loaded successfully!")
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()


# --------------------------------------------------
# 4. FACE DETECTOR
# --------------------------------------------------

@st.cache_resource
def load_face_detector():
    cascade_path = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    detector = cv2.CascadeClassifier(cascade_path)

    if detector.empty():
        raise RuntimeError("Could not load Haar Cascade.")

    return detector


try:
    face_detector = load_face_detector()
except Exception as e:
    st.error(f"Face detector error: {e}")
    st.stop()


# --------------------------------------------------
# 5. IMAGE PREPROCESSING
# --------------------------------------------------

def preprocess_face(face):

    gray_face = cv2.cvtColor(
        face,
        cv2.COLOR_BGR2GRAY
    )

    resized_face = cv2.resize(
        gray_face,
        (IMAGE_SIZE, IMAGE_SIZE)
    )

    normalized_face = (
        resized_face.astype("float32") / 255.0
    )

    processed_face = np.expand_dims(
        normalized_face,
        axis=-1
    )

    processed_face = np.expand_dims(
        processed_face,
        axis=0
    )

    return processed_face


# --------------------------------------------------
# 6. MODEL PREDICTION
# --------------------------------------------------

def predict_age_gender(face):

    processed_face = preprocess_face(face)

    predictions = model.predict(
        processed_face,
        verbose=0
    )

    if isinstance(predictions, dict):
        age_prediction = predictions["age_output"]
        gender_prediction = predictions["gender_output"]
    else:
        age_prediction = predictions[0]
        gender_prediction = predictions[1]

    age = float(np.array(age_prediction).reshape(-1)[0])

    gender_score = float(
        np.array(gender_prediction).reshape(-1)[0]
    )

    age = float(np.clip(age, 0, 116))

    if gender_score >= 0.5:
        gender = "Female"
        gender_class = 1
    else:
        gender = "Male"
        gender_class = 0

    return age, gender, gender_score, gender_class


# --------------------------------------------------
# 7. DETECT FACE
# --------------------------------------------------

def detect_largest_face(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40)
    )

    if len(faces) == 0:
        return None

    # Select largest detected face
    largest_face = max(
        faces,
        key=lambda rect: rect[2] * rect[3]
    )

    return largest_face


# --------------------------------------------------
# 8. PREDICTION DISPLAY
# --------------------------------------------------

def display_prediction(image_bytes):

    try:
        pil_image = Image.open(image_bytes).convert("RGB")
        rgb_image = np.array(pil_image)

        # Convert RGB to BGR for OpenCV
        image = cv2.cvtColor(
            rgb_image,
            cv2.COLOR_RGB2BGR
        )

        face_coordinates = detect_largest_face(image)

        if face_coordinates is None:
            st.warning(
                "No face detected. Please upload a clear "
                "front-facing face image."
            )
            return

        x, y, w, h = face_coordinates

        # Extract detected face
        face = image[y:y+h, x:x+w]

        if face.size == 0:
            st.error("Invalid face crop.")
            return

        # Predict
        age, gender, gender_score, gender_class = (
            predict_age_gender(face)
        )

        # Draw rectangle
        result_image = image.copy()

        cv2.rectangle(
            result_image,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        label = f"Age: {age:.1f} | {gender}"

        cv2.putText(
            result_image,
            label,
            (x, max(y-10, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # Convert BGR to RGB for Streamlit
        result_rgb = cv2.cvtColor(
            result_image,
            cv2.COLOR_BGR2RGB
        )

        # Display image
        st.image(
            result_rgb,
            caption="Face Detection and Prediction",
            width="stretch"
        )

        # Display results
        st.subheader("Prediction Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Predicted Age",
                value=f"{age:.1f} years"
            )

        with col2:
            st.metric(
                label="Predicted Gender Label",
                value=gender
            )

        st.write("Gender model output score:")

        st.progress(
            min(max(gender_score, 0.0), 1.0)
        )

        st.caption(
            f"Raw sigmoid score: {gender_score:.4f} | "
            f"Predicted class: {gender_class}"
        )

        st.info(
            "Note: The sigmoid score is a model output, "
            "not a calibrated confidence percentage. "
            "Predictions are estimates and may be inaccurate."
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")


# --------------------------------------------------
# 9. APP INTERFACE
# --------------------------------------------------

st.divider()

tab1, tab2 = st.tabs(
    ["📁 Upload Image", "📷 Webcam Capture"]
)


# --------------------------------------------------
# TAB 1: IMAGE UPLOAD
# --------------------------------------------------

with tab1:

    st.subheader("Upload Your Face Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            width="stretch"
        )

        if st.button(
            "Predict Age & Gender",
            key="upload_predict"
        ):

            display_prediction(uploaded_file)


# --------------------------------------------------
# TAB 2: WEBCAM CAPTURE
# --------------------------------------------------

with tab2:

    st.subheader("Capture Image Using Webcam")

    camera_image = st.camera_input(
        "Take a picture"
    )

    if camera_image is not None:

        if st.button(
            "Predict Webcam Image",
            key="camera_predict"
        ):

            display_prediction(camera_image)


# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Built using TensorFlow, Keras, OpenCV and Streamlit | "
    "Custom CNN trained on UTKFace"
)
