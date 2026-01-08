"""小说 AI 写作工坊 - 首页"""
import streamlit as st
from ui.components import render_sidebar_stats, init_session_state
from ui.pages.home import render as render_home

# 页面配置
st.set_page_config(
    page_title="小说 AI 写作工坊 - 首页",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
init_session_state()

# 渲染首页标题和导航
st.title("🏠 小说创作工作台")
st.markdown("---")

# 显示快速导航卡片
st.markdown("### 📑 功能导航")
st.markdown("点击下方按钮快速跳转到各个功能模块：")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    if st.button("📝 基本信息", use_container_width=True, type="primary", help="管理小说的基本信息（书名、简介、标签）"):
        st.switch_page("pages/1_基本信息.py")

with col2:
    if st.button("📋 剧情大纲", use_container_width=True, type="primary", help="管理整个小说的剧情大纲"):
        st.switch_page("pages/2_剧情大纲.py")

with col3:
    if st.button("⚙️ 设定管理", use_container_width=True, type="primary", help="管理世界观、修炼体系等设定"):
        st.switch_page("pages/3_设定管理.py")

with col4:
    if st.button("👤 角色管理", use_container_width=True, type="primary", help="管理角色卡和角色设定"):
        st.switch_page("pages/4_角色管理.py")

with col5:
    if st.button("📖 剧情状态", use_container_width=True, type="primary", help="管理当前剧情状态和进展"):
        st.switch_page("pages/5_剧情状态.py")

with col6:
    if st.button("📚 章节管理", use_container_width=True, type="primary", help="查看和管理已生成的章节"):
        st.switch_page("pages/6_章节管理.py")

st.markdown("---")

# 渲染首页内容（章节生成和章节目录）
render_home()

# 渲染侧边栏统计
render_sidebar_stats()
