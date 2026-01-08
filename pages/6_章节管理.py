"""章节管理页面 - 从首页的章节目录功能独立出来"""
import streamlit as st
from ui.components import render_sidebar_stats, init_session_state
from ui.pages.home import render_chapter_catalog

# 页面配置
st.set_page_config(
    page_title="章节管理",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
init_session_state()

# 返回首页按钮
if st.button("🔙 返回首页", use_container_width=False):
    st.switch_page("ui.py")

st.markdown("---")

# 渲染章节管理内容
st.title("📚 章节管理")
render_chapter_catalog()

# 渲染侧边栏统计
render_sidebar_stats()

