"""角色管理页面"""
import streamlit as st
from pathlib import Path
from ui.utils import get_files, save_file, delete_file

DATA_PATH = Path("data")


def render():
    """渲染角色管理页面"""
    st.title("👤 角色管理")
    st.markdown("---")
    
    char_dir = DATA_PATH / "characters"
    char_files = get_files(char_dir)
    
    # 操作选择
    operation = st.radio("操作", ["查看/编辑", "新建"], horizontal=True)
    
    if operation == "查看/编辑":
        _render_edit_view(char_files)
    else:
        _render_create_view(char_dir)


def _render_edit_view(char_files):
    """渲染编辑视图"""
    if char_files:
        selected_file = st.selectbox("选择角色卡", char_files, format_func=lambda x: x.stem)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            content = st.text_area(
                "内容",
                value=selected_file.read_text(encoding="utf-8"),
                height=400,
                key=f"char_edit_{selected_file.name}"
            )
        
        with col2:
            if st.button("💾 保存", type="primary", use_container_width=True):
                save_file(selected_file, content)
                st.success("保存成功！")
                st.rerun()
            
            if st.button("🗑️ 删除", use_container_width=True):
                delete_file(selected_file)
                st.success("删除成功！")
                st.rerun()
    else:
        st.info("暂无角色文件，请先创建")


def _render_create_view(char_dir):
    """渲染创建视图"""
    new_name = st.text_input("角色名（文件名）", value="", help="例如：shenyan、ahe、zhaojin")
    new_content = st.text_area(
        "角色卡内容",
        height=400,
        placeholder="# 角色卡：角色名\n\n- 身份：\n- 性格核心：\n- 行为风格：\n- 当前状态："
    )
    
    if st.button("✨ 创建", type="primary"):
        if new_name:
            new_file = char_dir / f"{new_name}.md"
            if new_file.exists():
                st.error("角色已存在，请使用其他名称")
            else:
                save_file(new_file, new_content)
                st.success("创建成功！")
                st.rerun()
        else:
            st.error("请输入角色名")

