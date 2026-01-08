"""基本信息管理页面"""
import streamlit as st
from pathlib import Path
from ui.utils import save_file

DATA_PATH = Path("data")


def parse_basic_info(content: str):
    """解析基本信息内容"""
    title = ""
    description = ""
    tags = []
    
    if content:
        lines = content.split('\n')
        current_section = None
        for line in lines:
            if line.strip().startswith('## 书名'):
                current_section = 'title'
            elif line.strip().startswith('## 简介'):
                current_section = 'description'
            elif line.strip().startswith('## 标签'):
                current_section = 'tags'
            elif current_section == 'title' and line.strip() and not line.startswith('#'):
                if not title:  # 只取第一行作为书名
                    title = line.strip()
            elif current_section == 'description' and line.strip() and not line.startswith('#'):
                description += line.strip() + '\n'
            elif current_section == 'tags' and line.strip() and not line.startswith('#'):
                tags = [t.strip() for t in line.strip().split(',') if t.strip()]
    
    return title, description, tags


def get_common_tags():
    """获取常见标签列表"""
    return [
        "玄幻", "奇幻", "武侠", "仙侠", "都市", "历史", "军事", "游戏",
        "竞技", "科幻", "悬疑", "轻小说", "二次元", "古代言情", "现代言情",
        "浪漫青春", "悬疑推理", "科幻未来", "游戏竞技", "二次元", "现实",
        "东方玄幻", "异世大陆", "王朝争霸", "高武世界", "末世危机", "未来世界",
        "都市生活", "商战职场", "娱乐明星", "校园青春", "婚恋家庭", "豪门世家",
        "古代情缘", "宫闱宅斗", "经商种田", "快穿", "系统", "重生", "穿越",
        "甜宠", "虐恋", "爽文", "升级流", "无敌流", "种田流", "无限流"
    ]


def render():
    """渲染基本信息管理页面"""
    st.title("📝 基本信息管理")
    st.markdown("---")
    
    basic_info_file = DATA_PATH / "basic_info.md"
    
    if basic_info_file.exists():
        content = basic_info_file.read_text(encoding="utf-8")
    else:
        content = "# 基本信息\n\n## 书名\n\n## 简介\n\n## 标签\n"
    
    # 解析基本信息
    title, description, tags = parse_basic_info(content)
    
    # 编辑界面
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📖 书名")
        novel_title = st.text_input("书名", value=title, placeholder="例如：灵气靖朝录", key="novel_title")
        
        st.subheader("📝 简介")
        novel_description = st.text_area(
            "简介",
            value=description.strip(),
            height=200,
            placeholder="请输入小说的简介...",
            key="novel_description"
        )
    
    with col2:
        st.subheader("🏷️ 标签")
        st.caption("参考番茄小说标签分类")
        
        # 多选标签
        selected_tags = st.multiselect(
            "选择标签（可多选）",
            options=get_common_tags(),
            default=tags,
            key="novel_tags"
        )
        
        # 自定义标签
        custom_tags = st.text_input(
            "自定义标签（用逗号分隔）",
            value="",
            placeholder="例如：修仙,升级,爽文",
            help="可以输入不在列表中的标签，用逗号分隔",
            key="custom_tags"
        )
        
        # 合并标签
        all_tags = selected_tags.copy()
        if custom_tags:
            all_tags.extend([t.strip() for t in custom_tags.split(',') if t.strip()])
    
    # 保存按钮
    if st.button("💾 保存基本信息", type="primary", use_container_width=True):
        saved_content = f"# 基本信息\n\n## 书名\n{novel_title}\n\n## 简介\n{novel_description}\n\n## 标签\n{', '.join(all_tags)}\n"
        save_file(basic_info_file, saved_content)
        st.success("✅ 保存成功！")
        st.rerun()
    
    # 显示当前基本信息预览
    st.markdown("---")
    st.subheader("📋 当前基本信息预览")
    col_preview1, col_preview2 = st.columns([1, 1])
    with col_preview1:
        st.markdown(f"**书名：** {novel_title if novel_title else '（未设置）'}")
        st.markdown(f"**标签：** {', '.join(all_tags) if all_tags else '（未设置）'}")
    with col_preview2:
        st.markdown(f"**简介：**")
        st.text(novel_description if novel_description else "（未设置）")

