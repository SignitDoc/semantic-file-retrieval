import streamlit as st
import os
import uuid
from streamlit_pdf_viewer import pdf_viewer


def preview_file(preview_file_path):
    file_ext = get_file_ext(preview_file_path)
    # 图片预览
    if file_ext in [".jpg", ".jpeg", ".png"]:
        st.image(preview_file_path)
    # txt/markdown预览
    elif file_ext in [".txt", ".md"]:
        with open(preview_file_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    # pdf预览
    elif file_ext == ".pdf":
        pdf_viewer(preview_file_path)


@st.dialog("预览", width="large")
def preview_file_with_dialog(*args):
    preview_file(*args)


def generate_file_uuid(file_name):
    """为文件名后追加6位uuid"""

    file_name_without_ext = os.path.splitext(file_name)[0]
    file_ext = os.path.splitext(file_name)[1]
    file_uuid = str(uuid.uuid4()).replace("-", "")[:6]
    return file_name_without_ext + "_" + file_uuid + file_ext


def get_file_ext(file_path):
    """获取文件后缀名"""

    return os.path.splitext(file_path)[-1]
