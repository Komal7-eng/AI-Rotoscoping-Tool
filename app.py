import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("AI Rotoscoping Tool")
st.write("Upload a photo — background removed instantly using AI")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    input_image = Image.open(uploaded_file)
    with col1:
        st.subheader("Original")
        st.image(input_image)
    
    with st.spinner("Removing background..."):
        output_data = remove(uploaded_file.getvalue())
        output_image = Image.open(io.BytesIO(output_data))
    
    with col2:
        st.subheader("Background removed")
        st.image(output_image)
    
    st.download_button(
        label="Download result",
        data=output_data,
        file_name="removed_bg.png",
        mime="image/png"
    )