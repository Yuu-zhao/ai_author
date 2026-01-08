"""设定管理页面"""
import streamlit as st
from pathlib import Path
from ui.utils import get_files, save_file, delete_file

DATA_PATH = Path("data")


def get_setting_templates():
    """获取设定模板"""
    return {
        "世界观设定": "# 世界观设定\n\n## 时代背景\n\n## 地理环境\n\n## 社会结构\n\n## 文化特色\n",
        "修炼体系": "# 修炼体系\n\n## 境界划分\n\n## 修炼方法\n\n## 特殊能力\n",
        "规则设定": "# 规则设定\n\n## 基本规则\n\n## 特殊规则\n\n## 限制条件\n",
        "其他设定": "# 设定\n\n## 说明\n\n"
    }


def render():
    """渲染设定管理页面"""
    st.title("⚙️ 设定管理")
    st.markdown("---")
    st.caption("管理世界观设定以及其他设定（如修炼体系、规则设定等）")
    
    settings_dir = DATA_PATH / "settings"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_files = get_files(settings_dir)
    
    # 操作选择
    operation = st.radio("操作", ["查看/编辑", "新建"], horizontal=True)
    
    if operation == "查看/编辑":
        _render_edit_view(settings_files, settings_dir)
    else:
        _render_create_view(settings_dir)


def _render_edit_view(settings_files, settings_dir):
    """渲染编辑视图"""
    if settings_files:
        selected_file = st.selectbox("选择设定文件", settings_files, format_func=lambda x: x.name)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            content = st.text_area(
                "设定内容",
                value=selected_file.read_text(encoding="utf-8"),
                height=400,
                key=f"settings_edit_{selected_file.name}",
                help="可以包含世界观设定、修炼体系、规则设定等"
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
        st.info("暂无设定文件，请先创建")


def _render_create_view(settings_dir):
    """渲染创建视图"""
    st.subheader("新建设定")
    new_name = st.text_input(
        "文件名（不含扩展名）",
        value="worldview",
        help="例如：worldview（世界观）、cultivation（修炼体系）、rules（规则设定）"
    )
    
    setting_type = st.selectbox(
        "设定类型",
        ["世界观设定", "修炼体系", "规则设定", "其他设定"],
        help="选择设定类型，便于分类管理"
    )
    
    templates = get_setting_templates()
    new_content = st.text_area(
        "设定内容",
        height=400,
        value=templates.get(setting_type, ""),
        key="new_setting_content"
    )
    
    if st.button("✨ 创建", type="primary"):
        if new_name:
            new_file = settings_dir / f"{new_name}.md"
            if new_file.exists():
                st.error("文件已存在，请使用其他名称")
            else:
                save_file(new_file, new_content)
                st.success("创建成功！")
                st.rerun()
        else:
            st.error("请输入文件名")

