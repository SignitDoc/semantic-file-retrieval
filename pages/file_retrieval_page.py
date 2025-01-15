import streamlit as st
from utils import get_file_ext, preview_file_with_dialog
from core.vector_db import retrieve_file, UPLOAD_DIR, retrieve_file_by_image
import os


# 文件语义检索界面
st.title("文件检索")

tab1, tab2, tab3 = st.tabs(["语义检索", "常规检索", "图片检索"])
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

with tab3:
    st.subheader("通过图片检索文件")
    uploaded_image = st.file_uploader(
        "上传一张图片用于检索", type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        # 显示上传的图片
        st.image(uploaded_image, caption="上传的图片", use_column_width=True)

        # 将上传的图片保存到临时位置（如果需要的话）
        image_path = os.path.join(UPLOAD_DIR, uploaded_image.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

        # 使用图片进行检索
        file_list = retrieve_file_by_image(image_path)

        st.divider()
        st.subheader("搜索结果(返回相关度最高的前三个结果)")

        for index, file_item in enumerate(file_list):
            file_name = file_item["file_name"]
            file_path = os.path.join(UPLOAD_DIR, file_name)
            ext = get_file_ext(file_name)
            st.markdown(f"{index+1}. **文件名：** {file_name}")
            st.markdown(f"**相关度：** {file_item['relevance']:.2%}")
            if ext.lower() in [".jpg", ".jpeg", ".png"]:
                st.image(file_path, caption=file_name)
            else:
                if st.button("预览", key=f"{file_name}_preview"):
                    preview_file_with_dialog(file_path)
            st.markdown("<br/>", unsafe_allow_html=True)
