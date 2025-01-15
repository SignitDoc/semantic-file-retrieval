import streamlit as st
import os
from utils import preview_file_with_dialog
from core.vector_db import my_collection, UPLOAD_DIR
from core.file_parser import (
    parse_image,
    parse_txt_or_md,
    parse_pdf,
    parse_mp4,
    parse_office,
)
from core.llm_processor import get_embedding
from utils import get_file_ext, preview_file

# 文件管理页面
st.title("文件管理")

tab1, tab2 = st.tabs(["文件上传", "文件列表"])

with tab1:
    uploaded_file = st.file_uploader(
        "选择要上传的文件",
        type=[
            "jpg",
            "jpeg",
            "png",
            "txt",
            "md",
            "pdf",
            "mp4",
            "docx",
            "xlsx",
            "pptx",
            ".doc",
            ".ppt",
            ".xls",
        ],
    )
    uploaded_file_path = ""
    if uploaded_file is not None:
        file_name = uploaded_file.name
        files = os.listdir(UPLOAD_DIR)
        if file_name in files:
            st.error(f"文件 {file_name} 已存在")
        else:
            with st.status("上传中，请稍等...", expanded=True) as status:
                st.write("1.正在保存文件...")
                uploaded_file_path = os.path.join(UPLOAD_DIR, file_name)
                file_ext = get_file_ext(uploaded_file_path)
                with open(uploaded_file_path, "wb") as f:
                    # 保存到本地
                    f.write(uploaded_file.getvalue())

                st.write("2.正在解析文件内容...")
                document_content = ""
                if file_ext in [".jpg", ".jpeg", ".png"]:
                    document_content = parse_image(uploaded_file_path)
                elif file_ext in [".txt", ".md"]:
                    document_content = parse_txt_or_md(uploaded_file_path)
                elif file_ext == ".pdf":
                    document_content = parse_pdf(uploaded_file_path)
                elif file_ext == ".mp4":
                    document_content = parse_mp4(uploaded_file_path)
                elif file_ext in [".docx", ".xlsx", ".pptx", ".doc", ".ppt", ".xls"]:
                    # 这个接口也可以处理pdf
                    document_content = parse_office(uploaded_file_path)
                else:
                    st.error("暂不支持该文件类型!")

                st.write("3.正在创建向量索引...")
                if document_content:
                    embedding = get_embedding(document_content)
                    my_collection.add(
                        documents=[document_content],
                        embeddings=[embedding],
                        ids=[file_name],  # 暂时用文件名作为id
                    )
                status.update(label="上传成功!", state="complete", expanded=False)

    st.divider()

    if uploaded_file_path:
        preview_file(uploaded_file_path)

with tab2:
    files = os.listdir(UPLOAD_DIR)
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file)
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.write(file)
        with col2:
            if st.button("删除", type="primary", key=f"{file}_delete"):
                os.remove(file_path)
                my_collection.delete(ids=[file])
                st.toast(f"文件 {file} 已删除")
                st.rerun()
        with col3:
            if st.button("预览", key=f"{file}_preview"):
                preview_file_with_dialog(file_path)
