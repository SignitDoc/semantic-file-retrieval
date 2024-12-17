import streamlit as st
import os
from utils import preview_file_with_dialog
from db import my_collection, UPLOAD_DIR


# 文件管理页面
st.title("文件管理")

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
            preview_file_with_dialog(file_path)
