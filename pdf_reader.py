import streamlit as st
import fitz  # PyMuPDF
from PIL import Image

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


def main():
    st.title("PDF Reader")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        images = convert_pdf_to_images(uploaded_file)

        for idx, image in enumerate(images):
            st.image(image, caption=f"Page {idx + 1}")


if __name__ == "__main__":
    main()
st.write("---")
st.write("This page is reserved. All rights reserved. :copyright:")

st.markdown("Credit : [Jasser](https://www.facebook.com/jasser.razzek.3/)")

