import streamlit as st
import os

from file_parser import parse_image, parse_txt_or_md, parse_pdf, get_embedding
from utils import preview_file, get_file_ext
from vector_db import my_collection

UPLOAD_DIR = "uploaded_files"

# 文件管理页面
st.title("文件管理")

uploaded_file = st.file_uploader(
    "选择要上传的文件",
    type=["jpg", "jpeg", "png", "txt", "md", "pdf"],
)
with st.spinner("正在上传..."):
    if uploaded_file is not None:
        uploaded_file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        file_ext = get_file_ext(uploaded_file_path)
        with open(uploaded_file_path, "wb") as f:
            # 保存到本地
            f.write(uploaded_file.getvalue())

        if file_ext in [".jpg", ".jpeg", ".png"]:
            document_content = parse_image(uploaded_file_path)
        elif file_ext in [".txt", ".md"]:
            document_content = parse_txt_or_md(uploaded_file_path)
        elif file_ext == ".pdf":
            document_content = parse_pdf(uploaded_file_path)
        else:
            st.error("暂不支持该文件类型!")

        if document_content:
            embedding = get_embedding(document_content)
            my_collection.add(
                documents=[document_content],
                embeddings=[embedding],
                ids=[uploaded_file_path],
            )
        st.toast(f"文件 {uploaded_file.name} 上传成功", icon="✅")

st.divider()


st.subheader("文件列表")


# 用列表展示本地uploaded_files目录下的所有文件，为每个文件提供预览和删除按钮
def show_file_list():
    files = os.listdir(UPLOAD_DIR)
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.write(file)
        with col2:
            if st.button("删除", type="primary", key=f"{file}_delete"):
                os.remove(file_path)
                my_collection.delete(ids=[file_path])
                st.toast(f"文件 {file} 已删除")
                st.rerun()
        with col3:
            if st.button("预览", key=f"{file}_preview"):
                preview_file(file_path)


show_file_list()
