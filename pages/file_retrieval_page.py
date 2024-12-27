import streamlit as st
from utils import get_file_ext, preview_file_with_dialog
from core.vector_db import retrieve_file, UPLOAD_DIR
import os


# 文件语义检索界面
st.title("文件检索")

tab1, tab2 = st.tabs(["语义检索", "常规检索"])
with tab1:
    query_text = st.text_input(
        "描述你想要搜索的文件(描述越详细返回结果越准确):",
        "",
        placeholder="例如:和张三签订的租房合同，租房地点在成都市青羊区",
    )

    st.divider()
    st.subheader("搜索结果(返回相关度最高的前三个结果)")

    if query_text:
        file_list = retrieve_file(query_text)
        for index, file_item in enumerate(file_list):
            file_name = file_item["file_name"]
            file_path = os.path.join(UPLOAD_DIR, file_name)
            ext = get_file_ext(file_name)
            st.html(f"{index+1}. <b>文件名：</b>{file_name}")
            st.html(f"<b>相关度：</b>{file_item['relevance']:.2%}")
            if ext in [".jpg", "jpeg", ".png"]:
                st.image(file_path, caption=file_name)
            else:
                if st.button("预览", key=f"{file_name}_preview"):
                    preview_file_with_dialog(file_path)
            st.html("<br/>")

with tab2:
    st.write("TODO")
