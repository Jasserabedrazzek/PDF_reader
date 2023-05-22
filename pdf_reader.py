import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import json
from datetime import datetime

st.set_page_config(
    page_title="PDF Reader",
    page_icon="📖",
    layout="centered")

def convert_pdf_to_images(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    num_pages = len(pdf)

    images = []
    for page_num in range(num_pages):
        page = pdf[page_num]
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(image)

    return images

def save_to_history(file_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history = load_history()
    history.append({
        "file_name": file_name,
        "timestamp": timestamp
    })
    with open("history.json", "w") as f:
        json.dump(history, f)

def load_history():
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    return history

def main():
    st.title("PDF Reader")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        images = convert_pdf_to_images(uploaded_file)
        file_name = uploaded_file.name
        save_to_history(file_name)

        for idx, image in enumerate(images):
            st.image(image, caption=f"Page {idx + 1}")

    if st.button("View History"):
        history = load_history()
        st.write("File upload history:")
        for record in history:
            st.write(f"File: {record['file_name']}, Timestamp: {record['timestamp']}")

if __name__ == "__main__":
    main()

st.write("---")
st.write("This page is reserved. All rights reserved. :copyright:")

st.markdown("Credit: [Jasser](https://www.facebook.com/jasser.razzek.3/)")
