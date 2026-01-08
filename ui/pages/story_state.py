"""剧情状态管理页面"""
import streamlit as st
from pathlib import Path
from ui.utils import save_file

DATA_PATH = Path("data")


def render():
    """渲染剧情状态管理页面"""
    st.title("📖 剧情状态管理")
    st.markdown("---")
    
    story_file = DATA_PATH / "plot" / "story_state.md"
    
    if story_file.exists():
        content = story_file.read_text(encoding="utf-8")
    else:
        content = "# 当前剧情状态\n\n## 已发生\n\n## 当前风险\n\n## 写作禁区\n"
    
    content = st.text_area(
        "剧情状态",
        value=content,
        height=500,
        help="记录当前剧情进展、已发生事件、风险和写作禁区",
        key="story_state_content"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💾 保存", type="primary", use_container_width=True):
            save_file(story_file, content)
            st.success("保存成功！")
            st.rerun()

