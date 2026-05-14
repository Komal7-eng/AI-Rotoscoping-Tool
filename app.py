import streamlit as st
from rembg import remove
from PIL import Image
import io
import cv2
import numpy as np
import tempfile
import os

st.set_page_config(page_title="AI Rotoscoping Tool", page_icon="🎬")
st.title("AI Rotoscoping Tool")
st.write("Built by a VFX Compositor | AI-powered background removal for images and video")

mode = st.radio("Select mode", ["Image", "Video"])

if mode == "Image":
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

elif mode == "Video":
    uploaded_video = st.file_uploader("Choose a video", type=["mp4", "mov", "avi"])
    if uploaded_video is not None:
        st.info("Video rotoscoping processes frame by frame — may take a few minutes")
        
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_video.read())
        tfile.close()

        cap = cv2.VideoCapture(tfile.name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        st.write(f"Video: {width}x{height} | {fps:.1f} fps | {total_frames} frames")

        if st.button("Start Rotoscoping"):
            output_frames = []
            progress = st.progress(0)
            status = st.empty()

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                
                img_bytes = io.BytesIO()
                pil_img.save(img_bytes, format='PNG')
                
                output_bytes = remove(img_bytes.getvalue())
                output_img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
                
                white_bg = Image.new("RGBA", output_img.size, (0, 0, 0, 255))
                white_bg.paste(output_img, mask=output_img.split()[3])
                frame_out = cv2.cvtColor(np.array(white_bg), cv2.COLOR_RGBA2BGR)
                output_frames.append(frame_out)

                frame_count += 1
                progress.progress(frame_count / total_frames)
                status.text(f"Processing frame {frame_count} of {total_frames}")

            cap.release()

            out_path = tempfile.mktemp(suffix='.mp4')
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            for f in output_frames:
                out.write(f)
            out.release()

            with open(out_path, 'rb') as f:
                video_bytes = f.read()

            st.success("Rotoscoping complete!")
            st.video(io.BytesIO(video_bytes))
            st.download_button("Download video", video_bytes, "rotoscoped.mp4", "video/mp4")

            os.unlink(tfile.name)
            os.unlink(out_path)
    else:
        st.info("Upload a short video clip to rotoscope it")