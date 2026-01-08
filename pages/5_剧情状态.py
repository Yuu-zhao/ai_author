"""剧情状态管理页面"""
import streamlit as st
from ui.components import render_sidebar_stats, init_session_state
from ui.pages.story_state import render as render_story_state

# 页面配置
st.set_page_config(
    page_title="剧情状态管理",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
init_session_state()

# 返回首页按钮
if st.button("🔙 返回首页", use_container_width=False):
    st.switch_page("ui.py")

st.markdown("---")

# 渲染页面内容
render_story_state()

# 渲染侧边栏统计
render_sidebar_stats()

