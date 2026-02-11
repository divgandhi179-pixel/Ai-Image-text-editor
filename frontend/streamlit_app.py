import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="AI Image Text Editor", layout="wide")

st.title("🖼️ AI Image Text Editor")
st.write("Upload an image (JPG, PNG) to begin.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    image_np = np.array(image)

    st.success("Image loaded successfully!")
