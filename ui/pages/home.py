"""首页模块 - 章节生成和管理"""
import streamlit as st
from pathlib import Path
from main import run_chapter
from writer.loader import (
    load_basic_info, load_settings, load_characters, load_story_state,
    load_outline, load_volume_outline, load_chapter_index
)
from writer.chapter_extractor import extract_chapter_summary, update_chapter_index
from writer.chapter_parser import parse_chapter_index, get_chapter_file_path
from writer.retriever import retrieve_relevant_characters
from writer.prompt_builder import build_prompt
from config import PROJECT_NAME, PROMPT_PATH
from ui.utils import get_files, save_file, delete_file

DATA_PATH = Path("data")


def render_chapter_detail_view():
    """渲染章节详情视图"""
    st.subheader(f"📖 {st.session_state.selected_chapter}")
    
    chapter_file = get_chapter_file_path(st.session_state.selected_chapter)
    if chapter_file:
        chapter_content = chapter_file.read_text(encoding="utf-8")
        
        # 分卷和概览管理
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            _render_chapter_summary(chapter_content)
        
        with col_info2:
            _render_volume_selection()
        
        # 章节内容编辑
        edited_content = st.text_area(
            "章节内容",
            value=chapter_content,
            height=400,
            key=f"content_{st.session_state.selected_chapter}"
        )
        
        # 操作按钮
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn1:
            if st.button("💾 保存章节", type="primary", use_container_width=True):
                _save_chapter(chapter_file, edited_content)
        
        with col_btn2:
            if st.button("🔙 返回列表", use_container_width=True):
                st.session_state.chapter_detail_view = False
                st.session_state.selected_chapter = None
                st.rerun()
        
        with col_btn3:
            if st.button("🗑️ 删除章节", use_container_width=True):
                delete_file(chapter_file)
                st.session_state.chapter_detail_view = False
                st.session_state.selected_chapter = None
                st.success("✅ 删除成功！")
                st.rerun()
        
        st.download_button(
            label="📥 下载章节",
            data=edited_content,
            file_name=chapter_file.name,
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.error("章节文件不存在")
        if st.button("🔙 返回列表"):
            st.session_state.chapter_detail_view = False
            st.session_state.selected_chapter = None
            st.rerun()


def _render_chapter_summary(chapter_content):
    """渲染章节概览部分"""
    index_data = parse_chapter_index()
    current_summary = ""
    
    # 查找当前章节的概览
    for vol, chapters in index_data["volumes"].items():
        for ch in chapters:
            if ch["chapter_no"] == st.session_state.selected_chapter:
                current_summary = ch["summary"]
                break
    
    if not current_summary:
        for ch in index_data["ungrouped"]:
            if ch["chapter_no"] == st.session_state.selected_chapter:
                current_summary = ch["summary"]
                break
    
    if not current_summary:
        current_summary = extract_chapter_summary(chapter_content, st.session_state.selected_chapter)
    
    chapter_summary = st.text_area(
        "📝 章节概览",
        value=current_summary,
        height=100,
        help="章节的简要概述，将显示在章节目录中",
        key=f"summary_{st.session_state.selected_chapter}"
    )
    
    if st.button("🔄 自动生成概览", use_container_width=True):
        auto_summary = extract_chapter_summary(chapter_content, st.session_state.selected_chapter)
        st.session_state[f"summary_{st.session_state.selected_chapter}"] = auto_summary
        st.rerun()


def _render_volume_selection():
    """渲染分卷选择部分"""
    volumes_dir = DATA_PATH / "plot" / "volumes"
    volumes = sorted([int(f.stem.split('_')[1]) for f in volumes_dir.glob("volume_*.md")]) if volumes_dir.exists() else []
    volume_options = ["无分卷"] + [f"第{vol}卷" for vol in volumes]
    
    index_data = parse_chapter_index()
    current_volume = None
    for vol, chapters in index_data["volumes"].items():
        for ch in chapters:
            if ch["chapter_no"] == st.session_state.selected_chapter:
                current_volume = ch["volume_no"]
                break
    
    default_vol_idx = 0
    if current_volume and current_volume in volumes:
        default_vol_idx = volumes.index(current_volume) + 1
    
    volume_key = f"volume_{st.session_state.selected_chapter}"
    selected_vol_str = st.selectbox(
        "📑 所属分卷",
        volume_options,
        index=default_vol_idx,
        key=volume_key
    )
    st.session_state[volume_key] = selected_vol_str


def _save_chapter(chapter_file, edited_content):
    """保存章节"""
    save_file(chapter_file, edited_content)
    
    # 更新概览
    summary_key = f"summary_{st.session_state.selected_chapter}"
    summary_text = st.session_state.get(summary_key, "")
    
    # 获取最新的分卷号
    volume_key = f"volume_{st.session_state.selected_chapter}"
    selected_vol_str = st.session_state.get(volume_key, "无分卷")
    volume_no_saved = None if selected_vol_str == "无分卷" else int(selected_vol_str.replace("第", "").replace("卷", ""))
    
    update_chapter_index(st.session_state.selected_chapter, summary_text, volume_no_saved)
    st.success("✅ 保存成功！")
    st.rerun()


def render_chapter_generation_view():
    """渲染章节生成视图"""
    st.subheader("✍️ 生成新章节")
    
    with st.expander("⚙️ 生成设置", expanded=False):
        show_prompt = st.checkbox("显示完整 Prompt", help="生成前预览完整的 Prompt 内容")
    
    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        chapter_no = st.text_input("📝 章节号", value="第13章", help="例如：第13章、Chapter_13", key="chapter_no_input")
        volume_no_input = st.number_input(
            "📑 所属分卷号（可选）",
            min_value=1,
            max_value=100,
            value=None,
            step=1,
            help="如果章节属于某个分卷，请输入分卷号",
            key="volume_no_input"
        )
    
    with col_gen2:
        _render_volume_quick_select()
    
    chapter_goal = st.text_area(
        "📋 本章写作目标",
        height=120,
        placeholder="例：衙门暗访，气氛逐渐收紧但未正面冲突\n\n描述本章要达成的剧情目标、氛围、关键事件等。",
        help="明确描述本章的写作目标，AI 会根据此目标结合现有设定生成内容",
        key="chapter_goal_input"
    )
    
    if st.button("🚀 开始生成章节", type="primary", use_container_width=True, icon="🚀"):
        _handle_chapter_generation(show_prompt)
    
    # 显示生成结果预览
    if st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📄 最新生成结果")
        with st.expander("查看内容", expanded=False):
            st.markdown(st.session_state.generated_content)


def _render_volume_quick_select():
    """渲染快速选择分卷"""
    volumes_dir = DATA_PATH / "plot" / "volumes"
    volumes = sorted([int(f.stem.split('_')[1]) for f in volumes_dir.glob("volume_*.md")]) if volumes_dir.exists() else []
    if volumes:
        selected_vol_str = st.selectbox(
            "或选择已有分卷",
            ["无",] + [f"第{vol}卷" for vol in volumes],
            key="volume_select_quick"
        )
        if selected_vol_str != "无":
            st.session_state["volume_no_input"] = int(selected_vol_str.replace("第", "").replace("卷", ""))


def _handle_chapter_generation(show_prompt):
    """处理章节生成"""
    chapter_no_val = st.session_state.chapter_no_input
    chapter_goal_val = st.session_state.chapter_goal_input
    volume_no_val = st.session_state.get("volume_no_input") or (
        int(st.session_state.get("volume_select_quick", "无").replace("第", "").replace("卷", ""))
        if st.session_state.get("volume_select_quick", "无") != "无" else None
    )
    
    if not chapter_no_val or not chapter_goal_val:
        st.error("请填写章节号和写作目标")
        return
    
    with st.spinner("正在生成章节，请稍候..."):
        try:
            # 显示 Prompt（如果勾选）
            if show_prompt:
                _show_prompt_preview(chapter_no_val, chapter_goal_val, volume_no_val)
            
            # 生成章节
            output_file = DATA_PATH / "chapters" / f"{chapter_no_val}.md"
            run_chapter(
                chapter_no=chapter_no_val,
                chapter_goal=chapter_goal_val,
                output_file=str(output_file),
                volume_no=int(volume_no_val) if volume_no_val else None
            )
            
            st.success(f"✅ 章节已生成：{chapter_no_val}")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            st.error(f"生成失败：{str(e)}")
            st.exception(e)


def _show_prompt_preview(chapter_no_val, chapter_goal_val, volume_no_val):
    """显示Prompt预览"""
    basic_info = load_basic_info()
    settings = load_settings()
    characters_all = load_characters()
    story_state = load_story_state()
    outline = load_outline()
    volume_outline = load_volume_outline(int(volume_no_val)) if volume_no_val else ""
    chapter_index = load_chapter_index()
    
    # 从基本信息中提取书名
    novel_name = PROJECT_NAME
    if basic_info and '## 书名' in basic_info:
        title_section = basic_info.split('## 书名')[1].split('##')[0] if '## 书名' in basic_info else ""
        title_lines = [l.strip() for l in title_section.split('\n') if l.strip() and not l.startswith('#')]
        if title_lines:
            novel_name = title_lines[0]
    
    characters = retrieve_relevant_characters(chapter_goal_val, characters_all)
    prompt = build_prompt(
        PROMPT_PATH,
        {
            "novel_name": novel_name,
            "basic_info": basic_info,
            "settings": settings,
            "characters": characters,
            "story_state": story_state,
            "outline": outline,
            "volume_outline": volume_outline,
            "chapter_index": chapter_index,
            "chapter_no": chapter_no_val,
            "chapter_goal": chapter_goal_val
        }
    )
    
    st.text_area("📝 Prompt 预览", prompt, height=300, disabled=True, key="prompt_preview")


def render_chapter_catalog():
    """渲染章节目录"""
    try:
        st.subheader("📚 章节目录")
        
        tab_catalog, tab_volumes = st.tabs(["📖 章节列表", "📑 分卷管理"])
        
        with tab_catalog:
            try:
                _render_chapter_list()
            except Exception as e:
                st.error(f"加载章节列表时出错：{str(e)}")
                st.exception(e)
                # 显示一个基本的错误恢复界面
                st.info("💡 如果问题持续，请检查 `data/plot/chapter_index.md` 文件")
        
        with tab_volumes:
            try:
                _render_volume_management()
            except Exception as e:
                st.error(f"加载分卷管理时出错：{str(e)}")
                st.exception(e)
                # 显示一个基本的错误恢复界面
                st.info("💡 如果问题持续，请检查 `data/plot/volumes/` 目录")
    except Exception as e:
        st.error(f"渲染章节目录时发生严重错误：{str(e)}")
        st.exception(e)
        st.info("💡 请刷新页面重试，或检查数据文件是否损坏")


def _render_chapter_list():
    """渲染章节列表"""
    try:
        index_data = parse_chapter_index()
    except Exception as e:
        st.error(f"解析章节目录失败：{str(e)}")
        st.info("请检查 `data/plot/chapter_index.md` 文件格式是否正确")
        return
    
    # 确保index_data有正确的结构
    if not isinstance(index_data, dict):
        st.error("章节目录数据格式错误")
        return
    
    volumes = index_data.get("volumes", {})
    ungrouped = index_data.get("ungrouped", [])
    
    # 显示分卷章节
    if volumes:
        try:
            # 安全地排序分卷号
            sorted_volumes = []
            for vol_num in volumes.keys():
                try:
                    sorted_volumes.append(int(vol_num))
                except (ValueError, TypeError):
                    # 如果无法转换为整数，跳过或使用字符串排序
                    continue
            
            sorted_volumes = sorted(sorted_volumes)
            
            for vol_num in sorted_volumes:
                vol_str = str(vol_num)
                if vol_str not in volumes:
                    continue
                    
                chapters = volumes[vol_str]
                if not isinstance(chapters, list):
                    continue
                    
                st.markdown(f"### 第{vol_num}卷")
                
                for ch in chapters:
                    if not isinstance(ch, dict):
                        continue
                    try:
                        _render_chapter_button(ch)
                    except Exception as e:
                        st.warning(f"渲染章节按钮时出错：{str(e)}")
                        continue
                
                st.markdown("---")
        except Exception as e:
            st.error(f"渲染分卷章节时出错：{str(e)}")
            st.exception(e)
    
    # 显示未分卷章节
    if ungrouped and isinstance(ungrouped, list):
        try:
            st.markdown("### 未分卷章节")
            for ch in ungrouped:
                if not isinstance(ch, dict):
                    continue
                try:
                    _render_chapter_button(ch)
                except Exception as e:
                    st.warning(f"渲染章节按钮时出错：{str(e)}")
                    continue
        except Exception as e:
            st.error(f"渲染未分卷章节时出错：{str(e)}")
    
    if not volumes and not ungrouped:
        _render_empty_chapter_list()


def _render_chapter_button(ch):
    """渲染章节按钮"""
    try:
        chapter_no = ch.get("chapter_no", "未知章节")
        summary = ch.get("summary", "")
        summary_preview = summary[:50] + "..." if len(summary) > 50 else summary
        
        chapter_button_key = f"btn_chapter_{chapter_no}"
        if st.button(
            f"**{chapter_no}**" + (f"\n💡 {summary_preview}" if summary else ""),
            key=chapter_button_key,
            help=summary if summary else "点击查看详情",
            use_container_width=True,
            type="primary" if st.session_state.selected_chapter == chapter_no else "secondary"
        ):
            st.session_state.selected_chapter = chapter_no
            st.session_state.chapter_detail_view = True
            st.rerun()
    except Exception as e:
        st.warning(f"渲染章节按钮失败：{str(e)}")


def _render_empty_chapter_list():
    """渲染空章节列表"""
    try:
        st.info("暂无章节，请先生成章节")
        
        # 从现有章节生成目录
        try:
            chapter_files = get_files(DATA_PATH / "chapters")
            if chapter_files:
                if st.button("🔄 从现有章节生成目录", use_container_width=True):
                    try:
                        index_file = DATA_PATH / "plot" / "chapter_index.md"
                        index_content = "# 章节目录\n\n本文件自动维护，包含所有章节的概要信息。\n\n"
                        
                        for cf in sorted(chapter_files):
                            try:
                                chapter_content = cf.read_text(encoding="utf-8")
                                chapter_no = cf.stem
                                summary = extract_chapter_summary(chapter_content, chapter_no)
                                index_content += f"- {chapter_no}：{summary}\n"
                            except Exception as e:
                                st.warning(f"处理章节文件 {cf.name} 时出错：{str(e)}")
                                continue
                        
                        save_file(index_file, index_content)
                        st.success("章节目录已生成！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"生成章节目录失败：{str(e)}")
        except Exception as e:
            st.warning(f"获取章节文件列表时出错：{str(e)}")
    except Exception as e:
        st.error(f"渲染空章节列表时出错：{str(e)}")


def _render_volume_management():
    """渲染分卷管理"""
    try:
        st.markdown("#### 📑 分卷管理")
        
        volumes_dir = DATA_PATH / "plot" / "volumes"
        volumes_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            volume_files = sorted(volumes_dir.glob("volume_*.md"), key=lambda x: int(x.stem.split('_')[1]))
        except (ValueError, IndexError) as e:
            st.warning(f"解析分卷文件名时出错：{str(e)}")
            volume_files = sorted(volumes_dir.glob("volume_*.md"), key=lambda x: x.name)
        
        if volume_files:
            try:
                selected_volume_file = st.selectbox(
                    "选择分卷",
                    volume_files,
                    format_func=lambda x: f"第{int(x.stem.split('_')[1])}卷" if '_' in x.stem else x.stem,
                    key="volume_select"
                )
                
                try:
                    volume_content = selected_volume_file.read_text(encoding="utf-8")
                except Exception as e:
                    st.error(f"读取分卷文件失败：{str(e)}")
                    volume_content = ""
                
                edited_volume = st.text_area(
                    "分卷细纲",
                    value=volume_content,
                    height=300,
                    key=f"volume_edit_{selected_volume_file.name}"
                )
                
                col_vol1, col_vol2 = st.columns(2)
                with col_vol1:
                    if st.button("💾 保存", use_container_width=True):
                        try:
                            save_file(selected_volume_file, edited_volume)
                            st.success("保存成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"保存失败：{str(e)}")
                
                with col_vol2:
                    if st.button("🗑️ 删除", use_container_width=True):
                        try:
                            delete_file(selected_volume_file)
                            st.success("删除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"删除失败：{str(e)}")
            except Exception as e:
                st.error(f"加载分卷列表时出错：{str(e)}")
        else:
            st.info("暂无分卷")
        
        st.markdown("---")
        st.markdown("#### ➕ 新建分卷")
        new_vol_no = st.number_input("分卷号", min_value=1, max_value=100, value=1, step=1, key="new_vol_no")
        new_vol_content = st.text_area(
            "分卷细纲",
            height=200,
            placeholder=f"# 第{new_vol_no}卷 细纲\n\n## 分卷主线\n\n## 主要情节\n\n## 角色发展\n",
            key="new_vol_content"
        )
        
        if st.button("✨ 创建分卷", use_container_width=True):
            try:
                new_vol_file = volumes_dir / f"volume_{new_vol_no:02d}.md"
                if new_vol_file.exists():
                    st.error("该分卷已存在")
                else:
                    save_file(new_vol_file, new_vol_content)
                    st.success("创建成功！")
                    st.rerun()
            except Exception as e:
                st.error(f"创建分卷失败：{str(e)}")
    except Exception as e:
        st.error(f"渲染分卷管理时出错：{str(e)}")
        st.exception(e)


def render():
    """渲染首页"""
    try:
        st.title("🏠 小说创作工作台")
        
        # 左右分栏布局
        main_col1, main_col2 = st.columns([1.2, 1])
        
        with main_col1:
            try:
                if st.session_state.chapter_detail_view and st.session_state.selected_chapter:
                    render_chapter_detail_view()
                else:
                    render_chapter_generation_view()
            except Exception as e:
                st.error(f"渲染左侧内容时出错：{str(e)}")
                st.exception(e)
        
        with main_col2:
            try:
                render_chapter_catalog()
            except Exception as e:
                st.error(f"渲染右侧章节目录时出错：{str(e)}")
                st.exception(e)
    except Exception as e:
        st.error(f"渲染首页时发生严重错误：{str(e)}")
        st.exception(e)
        st.info("💡 请刷新页面重试")

