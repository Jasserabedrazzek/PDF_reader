import streamlit as st
import fitz  # PyMuPDF
from PIL import Image

st.set_page_config(
    page_title="PDF Reader",
    page_icon="📖",
    layout="centered"
)

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

def zoom_image(image, zoom_factor):
    width, height = image.size
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def main():
    st.title("PDF Reader")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        images = convert_pdf_to_images(uploaded_file)

        zoom_factor = 1.0  # Initial zoom factor

        for idx, image in enumerate(images):
            zoomed_image = zoom_image(image, zoom_factor)
            st.image(zoomed_image, caption=f"Page {idx + 1}")

        st.write("---")
        st.write("This page is reserved. All rights reserved. \u00A9")

        # Zoom buttons
        st.write("Zoom:")
        zoom_in = st.button("Zoom In")
        zoom_out = st.button("Zoom Out")

        # Handle button clicks
        if zoom_in:
            zoom_factor += 0.1
            st.caching.clear_cache()  # Clear the cache to update the displayed images

        if zoom_out:
            zoom_factor -= 0.1
            if zoom_factor < 0.1:
                zoom_factor = 0.1
            st.caching.clear_cache()  # Clear the cache to update the displayed images

if __name__ == "__main__":
    main()
