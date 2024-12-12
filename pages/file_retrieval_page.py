import streamlit as st
from utils import preview_file
from vector_db import retrieve_file

# 文件语义检索界面
st.title("语义检索")

query_text = st.text_input(
    "描述你想要搜索的文件(描述越详细返回结果越准确):",
    "",
    placeholder="例如:和张三签订的租房合同，租房地点在成都市青羊区",
)

st.divider()
st.subheader("搜索结果(返回相关度最高的三个结果)")

col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    st.write("文件名")
with col2:
    st.write("相关度")
with col3:
    st.write("操作")

if query_text:
    file_list = retrieve_file(query_text)
    col1, col2, col3 = st.columns([5, 1, 1])
    for file_item in file_list:
        file_path = file_item["file_path"]
        with col1:
            st.write(file_path)
        with col2:
            st.write(f"{file_item['relevance']:.2%}")
        with col3:
            if st.button("预览", key=f"{file_path}_preview"):
                preview_file(file_path)
