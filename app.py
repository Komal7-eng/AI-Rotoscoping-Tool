import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="AI Rotoscoping Tool", page_icon="🎬")
st.title("AI Rotoscoping Tool")
st.write("Built by a VFX Compositor | Remove backgrounds instantly using AI")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    input_image = Image.open(uploaded_file)
    with col1:
        st.subheader("Original")
        st.image(input_image, width=300)
    with st.spinner("AI removing background..."):
        output_bytes = remove(uploaded_file.getvalue())
        output_image = Image.open(io.BytesIO(output_bytes))
    with col2:
        st.subheader("Background removed")
        st.image(output_image, width=300)
    st.success("Done!")
    st.download_button("Download PNG", output_bytes, "result.png", "image/png")
else:
    st.info("Upload a JPG or PNG to get started")