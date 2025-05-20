import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Brigruk Card Centering Analyzer", layout="centered")
st.title("Brigruk Card Centering Analyzer")
st.markdown("Upload one or more images of your card with the Brigruk tool. We'll analyze the centering for you.")

uploaded_files = st.file_uploader("Choose card images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Analyzing cards..."):
        files = [("images", (file.name, file, file.type)) for file in uploaded_files]
        try:
            response = requests.post("http://localhost:5000/batch-analyze", files=files)
            data = response.json()
        except Exception as e:
            st.error("Failed to connect to the analysis server.")
            st.stop()

    for result in data:
        st.subheader(f"Results for: {result['filename']}")
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"Horizontal Centering: {result['horizontal_ratio']} ({result['horizontal_score']}%)")
            st.success(f"Vertical Centering: {result['vertical_ratio']} ({result['vertical_score']}%)")
            st.info(f"Confidence: {result['confidence']}%")
            st.markdown(f"**Brigruk Numbers**: Top: {result['brigruk_numbers']['top']}, Bottom: {result['brigruk_numbers']['bottom']}, Left: {result['brigruk_numbers']['left']}, Right: {result['brigruk_numbers']['right']}")