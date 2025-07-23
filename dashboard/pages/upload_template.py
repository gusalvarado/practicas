import os
import sys
from pathlib import Path
import streamlit as st
from theme import theme

theme()

sys.path.append(str(Path(__file__).resolve().parents[2]))
from utils.s3_uploader import upload_file

st.set_page_config(page_title="Upload Template", page_icon="/assets/favicon.png")
st.title("Upload Template")

bucket = os.getenv("S3_BUCKET")
upload_prefix = "templates"

upload_file = st.file_uploader("Upload template file:")

if upload_file is not None:
    filename = upload_file.name
    content = upload_file.getvalue()

    if st.button("Upload"):
        try:
            s3_key = f"{upload_prefix}/{filename}"
            url = upload_file(bucket, s3_key, content)
            st.success(f"File uploaded successfully to {url}")
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")