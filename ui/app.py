"""主应用入口"""
import streamlit as st
from ui.components import render_sidebar_navigation, render_sidebar_stats, init_session_state
from ui.router import get_current_route
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

# 获取当前路由
current_route = get_current_route()

# 路由映射
route_map = {
    "home": render_home,
    "basic_info": render_basic_info,
    "outline": render_outline,
    "settings": render_settings,
    "characters": render_characters,
    "story_state": render_story_state
}

# 路由到对应页面
render_func = route_map.get(current_route, render_home)
try:
    render_func()
except Exception as e:
    st.error(f"渲染页面时出错：{str(e)}")
    st.exception(e)

# 渲染侧边栏统计
render_sidebar_stats()

