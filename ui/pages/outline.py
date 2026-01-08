"""剧情大纲管理页面"""
import streamlit as st
from pathlib import Path
from ui.utils import save_file

DATA_PATH = Path("data")


def render():
    """渲染剧情大纲管理页面"""
    st.title("📋 剧情大纲管理")
    st.markdown("---")
    
    outline_file = DATA_PATH / "plot" / "outline.md"
    
    if outline_file.exists():
        content = outline_file.read_text(encoding="utf-8")
    else:
        content = "# 剧情大纲\n\n## 整体主线\n\n## 核心冲突\n\n## 主要转折点\n\n## 结局走向\n"
    
    content = st.text_area(
        "剧情大纲",
        value=content,
        height=500,
        help="设定整个小说的剧情大纲，包括主线、冲突、转折点等",
        key="outline_content"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💾 保存", type="primary", use_container_width=True):
            save_file(outline_file, content)
            st.success("保存成功！")
            st.rerun()

