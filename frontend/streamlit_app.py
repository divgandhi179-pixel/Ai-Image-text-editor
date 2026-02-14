import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import easyocr
import cv2

st.set_page_config(page_title="AI Image Text Editor", layout="wide")

st.title("🖼️ AI Image Text Editor")
st.write("Upload an image (JPG, PNG) to detect and replace text.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image, caption="Original Image", use_column_width=True)

    # Run OCR only once
    if "ocr_results" not in st.session_state:
        st.info("Running OCR...")
        reader = easyocr.Reader(['en'], gpu=False)
        st.session_state.ocr_results = reader.readtext(image_np)

    results = st.session_state.ocr_results

    if len(results) == 0:
        st.warning("No text detected.")
    else:
        detected_texts = [text for (bbox, text, conf) in results]

        selected_text = st.selectbox("Select text to replace:", detected_texts)
        new_text = st.text_input("Enter new text:")

        if st.button("Replace Text") and new_text:

            image_copy = image_np.copy()

            for (bbox, text, conf) in results:
                if text == selected_text:

                    top_left = tuple(map(int, bbox[0]))
                    bottom_right = tuple(map(int, bbox[2]))

                    # Remove old text
                    cv2.rectangle(image_copy, top_left, bottom_right, (255, 255, 255), -1)

                    # Calculate dynamic font size
                    box_height = bottom_right[1] - top_left[1]
                    font_size = int(box_height * 0.8)

                    pil_img = Image.fromarray(image_copy)
                    draw = ImageDraw.Draw(pil_img)

                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()

                    draw.text(top_left, new_text, fill="black", font=font)

                    image_copy = np.array(pil_img)

            st.image(image_copy, caption="Edited Image", use_column_width=True)
            st.success("Text Replaced Successfully!")
