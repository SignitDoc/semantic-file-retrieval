import streamlit as st

# 隐藏右上角deploy按钮和mainmenu
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .stAppDeployButton {display: none;}
        div[role="dialog"] {width:980px;}
    </style>
""",
    unsafe_allow_html=True,
)

app = st.navigation(
    [
        st.Page("pages/file_uploading_page.py", title="文件上传"),
        st.Page("pages/file_management_page.py", title="文件管理"),
        st.Page("pages/file_retrieval_page.py", title="语义检索"),
    ]
)
app.run()
