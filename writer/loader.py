from pathlib import Path

def load_folder_md(path):
    texts = []
    for file in Path(path).glob("*.md"):
        texts.append(file.read_text(encoding="utf-8"))
    return "\n\n".join(texts)

def load_world():
    return load_folder_md("data/world")

def load_characters():
    return load_folder_md("data/characters")

def load_story_state():
    story_file = Path("data/plot/story_state.md")
    if story_file.exists():
        return story_file.read_text(encoding="utf-8")
    return ""

def load_outline():
    """加载剧情大纲"""
    outline_file = Path("data/plot/outline.md")
    if outline_file.exists():
        return outline_file.read_text(encoding="utf-8")
    return ""

def load_volume_outline(volume_no):
    """加载指定分卷的细纲"""
    volume_file = Path(f"data/plot/volumes/volume_{volume_no:02d}.md")
    if volume_file.exists():
        return volume_file.read_text(encoding="utf-8")
    return ""

def load_chapter_index():
    """加载章节目录和情节概要"""
    index_file = Path("data/plot/chapter_index.md")
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return ""

def load_basic_info():
    """加载基本信息（书名、简介、标签）"""
    basic_info_file = Path("data/basic_info.md")
    if basic_info_file.exists():
        return basic_info_file.read_text(encoding="utf-8")
    return ""

def load_settings():
    """加载设定（包括世界观和其他设定）"""
    settings_dir = Path("data/settings")
    if not settings_dir.exists():
        settings_dir.mkdir(parents=True, exist_ok=True)
    return load_folder_md(settings_dir)

