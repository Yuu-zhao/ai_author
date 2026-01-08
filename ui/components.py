"""UI公共组件模块"""
import streamlit as st
from pathlib import Path
from ui.utils import get_files

DATA_PATH = Path("data")


def render_sidebar_navigation():
    """渲染侧边栏导航"""
    st.sidebar.title("📖 小说 AI 写作工坊")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "导航",
        [
            "🏠 首页",
            "📝 基本信息",
            "📋 剧情大纲",
            "⚙️ 设定管理",
            "👤 角色管理",
            "📖 剧情状态"
        ]
    )
    return page


def render_sidebar_stats():
    """渲染侧边栏统计信息"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 数据统计")
    st.sidebar.metric("设定", len(get_files(DATA_PATH / "settings")))
    st.sidebar.metric("角色", len(get_files(DATA_PATH / "characters")))
    st.sidebar.metric("章节", len(get_files(DATA_PATH / "chapters")))
    
    # 统计分卷数量
    volumes_dir = DATA_PATH / "plot" / "volumes"
    if volumes_dir.exists():
        volume_count = len(get_files(volumes_dir))
    else:
        volume_count = 0
    st.sidebar.metric("分卷", volume_count)
    
    # 检查是否存在基本信息、大纲和目录
    basic_info_exists = "✅" if (DATA_PATH / "basic_info.md").exists() else "❌"
    outline_exists = "✅" if (DATA_PATH / "plot" / "outline.md").exists() else "❌"
    index_exists = "✅" if (DATA_PATH / "plot" / "chapter_index.md").exists() else "❌"
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 状态")
    st.sidebar.markdown(f"基本信息：{basic_info_exists}")
    st.sidebar.markdown(f"剧情大纲：{outline_exists}")
    st.sidebar.markdown(f"章节目录：{index_exists}")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("💡 提示：所有数据直接保存在 `data/` 目录")


def init_session_state():
    """初始化session state"""
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = ""
    if 'selected_chapter' not in st.session_state:
        st.session_state.selected_chapter = None
    if 'chapter_detail_view' not in st.session_state:
        st.session_state.chapter_detail_view = False

