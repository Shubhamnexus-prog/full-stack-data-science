
import streamlit as st
import numpy as np
import cv2
import os

from pathlib import Path
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from tensorflow.keras.models import load_model


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CNN Digit Recognition",
    page_icon="🔢",
    layout="wide"
)

st.title("🔢 Handwritten Digit Recognition")
st.markdown(
    "### Draw a digit (0-9) or upload an image and let CNN predict it."
)

st.divider()


# ==========================================
# 2. MODEL LOADING
# ==========================================

MODEL_PATH = Path(
    r"E:\full stack data science\deep learning\CNN\digits recogniation\digit_recognition_model.keras"
)


@st.cache_resource
def load_cnn_model():

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return load_model(str(MODEL_PATH))


try:
    model = load_cnn_model()
    st.success("CNN Model Loaded Successfully!")

except Exception as e:
    st.error(f"Model Loading Error: {e}")
    st.stop()


# ==========================================
# 3. IMAGE PREPROCESSING
# ==========================================

def preprocess_image(image):

    # Convert image to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(
            image.astype(np.uint8),
            cv2.COLOR_RGB2GRAY
        )
    else:
        gray = image.astype(np.uint8)

    # Threshold image
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Detect foreground/background using border pixels
    border = np.concatenate([
        thresh[0, :],
        thresh[-1, :],
        thresh[:, 0],
        thresh[:, -1]
    ])

    # Make digit white and background black
    if np.mean(border) > 127:
        thresh = 255 - thresh

    # Find digit boundaries
    coords = cv2.findNonZero(thresh)

    if coords is None:
        return None

    x, y, w, h = cv2.boundingRect(coords)

    digit = thresh[y:y+h, x:x+w]

    # Resize digit while preserving aspect ratio
    scale = 20.0 / max(w, h)

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = cv2.resize(
        digit,
        (new_w, new_h),
        interpolation=cv2.INTER_AREA
    )

    # Create 28x28 black background
    canvas = np.zeros((28, 28), dtype=np.uint8)

    # Place digit in center
    x_offset = (28 - new_w) // 2
    y_offset = (28 - new_h) // 2

    canvas[
        y_offset:y_offset + new_h,
        x_offset:x_offset + new_w
    ] = resized

    # Normalize
    canvas = canvas.astype("float32") / 255.0

    return canvas


# ==========================================
# 4. MODEL INPUT SHAPE
# ==========================================

def prepare_model_input(processed_image):

    input_shape = model.input_shape

    if isinstance(input_shape, list):
        input_shape = input_shape[0]

    if len(input_shape) == 4:
        # CNN: (None, 28, 28, 1)
        return processed_image.reshape(1, 28, 28, 1)

    elif len(input_shape) == 3:
        # (None, 28, 28)
        return processed_image.reshape(1, 28, 28)

    elif len(input_shape) == 2:
        # Flattened model: (None, 784)
        return processed_image.reshape(1, 784)

    else:
        raise ValueError(
            f"Unsupported model input shape: {input_shape}"
        )


# ==========================================
# 5. PREDICTION FUNCTION
# ==========================================

def predict_digit(processed_image):

    model_input = prepare_model_input(processed_image)

    prediction = model.predict(
        model_input,
        verbose=0
    )

    probabilities = prediction[0]

    predicted_digit = int(np.argmax(probabilities))

    confidence = float(
        probabilities[predicted_digit] * 100
    )

    return predicted_digit, confidence, probabilities


# ==========================================
# 6. DISPLAY PREDICTION
# ==========================================

def show_prediction(image):

    processed_image = preprocess_image(image)

    if processed_image is None:
        st.warning("No digit detected. Please draw or upload a digit.")
        return

    digit, confidence, probabilities = predict_digit(
        processed_image
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Processed Image")

        st.image(
            processed_image,
            width=200,
            clamp=True
        )

    with col2:

        st.subheader("Prediction")

        st.success(f"Predicted Digit: {digit}")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.progress(
            max(0.0, min(1.0, confidence / 100))
        )

    st.subheader("All Digit Probabilities")

    st.bar_chart({
        str(i): float(probabilities[i] * 100)
        for i in range(len(probabilities))
    })


# ==========================================
# 7. DRAWING CANVAS
# ==========================================

st.header("✍️ Draw Your Digit")

st.write("Draw any digit between 0 and 9 inside the white canvas.")

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0

canvas_col, info_col = st.columns([1, 1])

with canvas_col:

    canvas_result = st_canvas(

        fill_color="rgba(255, 255, 255, 1)",

        stroke_width=18,

        stroke_color="#000000",

        background_color="#FFFFFF",

        height=280,

        width=280,

        drawing_mode="freedraw",

        update_streamlit=True,

        key=f"digit_canvas_{st.session_state.canvas_version}",

        return_image_data=True
    )

with info_col:

    st.markdown("### Instructions")

    st.write("1. Draw a single digit.")
    st.write("2. Keep the digit near the center.")
    st.write("3. Click Predict Digit.")
    st.write("4. See the CNN prediction.")

    st.info("Tip: Draw clearly using a thick black stroke.")


# ==========================================
# 8. CANVAS BUTTONS
# ==========================================

predict_col, clear_col = st.columns(2)

with predict_col:

    predict_button = st.button(
        "🔍 Predict Digit",
        use_container_width=True
    )

with clear_col:

    clear_button = st.button(
        "🗑️ Clear Canvas",
        use_container_width=True
    )


if clear_button:

    st.session_state.canvas_version += 1

    st.rerun()


if predict_button:

    if canvas_result.image_data is None:

        st.warning("Please draw a digit first!")

    else:

        # Canvas returns RGBA image data
        canvas_image = canvas_result.image_data

        # Convert to uint8 RGB
        canvas_image = np.clip(
            canvas_image[:, :, :3],
            0,
            255
        ).astype(np.uint8)

        # Convert white background and black strokes
        # into black background and white digit
        gray_image = cv2.cvtColor(
            canvas_image,
            cv2.COLOR_RGB2GRAY
        )

        # Prediction
        show_prediction(gray_image)


# ==========================================
# 9. IMAGE UPLOAD PREDICTION
# ==========================================

st.divider()

st.header("📤 Upload Digit Image")

uploaded_file = st.file_uploader(
    "Upload a handwritten digit image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    uploaded_image = Image.open(
        uploaded_file
    ).convert("RGB")

    uploaded_array = np.array(uploaded_image)

    st.subheader("Uploaded Image")

    st.image(
        uploaded_image,
        width=250
    )

    if st.button(
        "Predict Uploaded Image",
        use_container_width=True
    ):

        show_prediction(uploaded_array)


# ==========================================
# 10. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center">
        <h4>Built with Python, Streamlit, TensorFlow & CNN</h4>
        <p>Handwritten Digit Recognition | Deep Learning Project</p>
    </div>
    """,
    unsafe_allow_html=True
)
