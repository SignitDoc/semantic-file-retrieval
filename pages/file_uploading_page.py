import streamlit as st
import os
from file_parser import parse_image, parse_txt_or_md, parse_pdf, get_embedding
from utils import get_file_ext, preview_file
from db import my_collection, UPLOAD_DIR


st.title("文件上传")

uploaded_file = st.file_uploader(
    "选择要上传的文件",
    type=["jpg", "jpeg", "png", "txt", "md", "pdf"],
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
