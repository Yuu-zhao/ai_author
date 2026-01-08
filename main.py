from config import PROJECT_NAME, PROMPT_PATH
from writer.loader import (
    load_world, load_characters, load_story_state,
    load_outline, load_volume_outline, load_chapter_index,
    load_basic_info, load_settings
)
from writer.retriever import retrieve_relevant_characters
from writer.prompt_builder import build_prompt
from writer.generator import generate_chapter
from writer.chapter_extractor import extract_chapter_summary, update_chapter_index

def run_chapter(chapter_no, chapter_goal, output_file, volume_no=None):
    # 加载基本信息
    basic_info = load_basic_info()
    # 从基本信息中提取书名（如果存在）
    novel_name = PROJECT_NAME
    if basic_info and '## 书名' in basic_info:
        try:
            title_section = basic_info.split('## 书名')[1].split('##')[0] if '## 书名' in basic_info else ""
            title_lines = [l.strip() for l in title_section.split('\n') if l.strip() and not l.startswith('#')]
            if title_lines:
                novel_name = title_lines[0]
        except:
            pass
    
    # 加载设定（替代原来的world）
    settings = load_settings()
    characters_all = load_characters()
    story_state = load_story_state()
    outline = load_outline()
    volume_outline = load_volume_outline(volume_no) if volume_no else ""
    chapter_index = load_chapter_index()

    characters = retrieve_relevant_characters(
        chapter_goal,
        characters_all
    )

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
            "chapter_no": chapter_no,
            "chapter_goal": chapter_goal
        }
    )

    text = generate_chapter(prompt)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    # 提取并更新章节概要
    summary = extract_chapter_summary(text, chapter_no)
    update_chapter_index(chapter_no, summary, volume_no)

    print(f"{chapter_no} 已生成")

if __name__ == "__main__":
    run_chapter(
        chapter_no="第13章",
        chapter_goal="衙门暗访，气氛逐步收紧但未正面冲突",
        output_file="data/chapters/chapter_013.md"
    )

