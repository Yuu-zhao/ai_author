"""主应用入口"""
import streamlit as st
from ui.components import render_sidebar_navigation, render_sidebar_stats, init_session_state
from ui.pages import (
    render_home,
    render_basic_info,
    render_outline,
    render_settings,
    render_characters,
    render_story_state
)

# 页面配置
st.set_page_config(
    page_title="小说 AI 写作工坊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
init_session_state()

# 渲染侧边栏导航
page = render_sidebar_navigation()

# 路由到对应页面
if page == "🏠 首页":
    render_home()
elif page == "📝 基本信息":
    render_basic_info()
elif page == "📋 剧情大纲":
    render_outline()
elif page == "⚙️ 设定管理":
    render_settings()
elif page == "👤 角色管理":
    render_characters()
elif page == "📖 剧情状态":
    render_story_state()

# 渲染侧边栏统计
render_sidebar_stats()

