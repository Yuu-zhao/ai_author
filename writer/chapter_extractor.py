"""章节概要提取工具"""
import re
from pathlib import Path

def extract_chapter_summary(chapter_content, chapter_no):
    """
    从章节内容中提取概要
    
    如果章节包含明确的概要标记，则提取；否则生成一个简要描述
    """
    # 尝试提取章节开头的概要（如果有特殊标记）
    summary_patterns = [
        r'##?\s*概要[：:]\s*(.+?)(?:\n\n|\n#|$)',
        r'##?\s*情节概要[：:]\s*(.+?)(?:\n\n|\n#|$)',
        r'##?\s*本章要点[：:]\s*(.+?)(?:\n\n|\n#|$)',
    ]
    
    for pattern in summary_patterns:
        match = re.search(pattern, chapter_content, re.DOTALL | re.IGNORECASE)
        if match:
            summary = match.group(1).strip()
            # 清理多余的换行和空格
            summary = re.sub(r'\n+', ' ', summary)
            summary = re.sub(r'\s+', ' ', summary)
            return summary[:200]  # 限制长度
    
    # 如果没有明确标记，尝试提取前几段作为概要
    paragraphs = chapter_content.split('\n\n')
    non_empty_paragraphs = [p.strip() for p in paragraphs if p.strip() and not p.strip().startswith('#')]
    
    if non_empty_paragraphs:
        # 取前2-3段，限制总长度
        summary = ' '.join(non_empty_paragraphs[:3])[:200]
        return summary
    
    return "（暂无概要）"

def update_chapter_index(chapter_no, chapter_summary, volume_no=None):
    """
    更新章节目录索引
    
    Args:
        chapter_no: 章节号（如"第1章"）
        chapter_summary: 章节概要
        volume_no: 所属分卷号（可选）
    """
    index_file = Path("data/plot/chapter_index.md")
    index_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有索引
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
    else:
        content = "# 章节目录\n\n本文件自动维护，包含所有章节的概要信息。\n\n"
    
    # 检查章节是否已存在
    pattern = rf'^\s*-\s*{re.escape(chapter_no)}'
    lines = content.split('\n')
    found = False
    new_lines = []
    
    for line in lines:
        if re.match(pattern, line):
            # 替换现有条目
            volume_str = f" [卷{volume_no}]" if volume_no else ""
            new_lines.append(f"- {chapter_no}{volume_str}：{chapter_summary}")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        # 添加新条目（按章节号插入到合适位置）
        volume_str = f" [卷{volume_no}]" if volume_no else ""
        new_entry = f"- {chapter_no}{volume_str}：{chapter_summary}"
        
        # 如果已有分卷标记，按分卷插入；否则插入到末尾
        if volume_no:
            # 找到对应分卷的插入位置
            insert_pos = len(new_lines)
            target_volume_found = False
            current_volume = None
            
            for i, line in enumerate(new_lines):
                if line.strip().startswith('## 第') and '卷' in line:
                    vol_match = re.search(r'第(\d+)卷', line)
                    if vol_match:
                        current_volume = int(vol_match.group(1))
                        if current_volume == volume_no:
                            target_volume_found = True
                        elif current_volume > volume_no and not target_volume_found:
                            # 需要在当前分卷之前插入新分卷
                            insert_pos = i
                            break
                elif line.strip().startswith('-') and target_volume_found:
                    volume_match = re.search(r'\[卷(\d+)\]', line)
                    if volume_match:
                        vol = int(volume_match.group(1))
                        if vol != volume_no:
                            # 已到下一个分卷，在当前分卷末尾插入
                            insert_pos = i
                            break
                        insert_pos = i + 1
                elif line.strip().startswith('-') and current_volume is None:
                    # 没有分卷标记，但当前行有章节，检查是否需要插入分卷
                    insert_pos = i
                    break
            
            # 如果没找到对应分卷，需要创建分卷标题
            if not target_volume_found:
                # 检查是否需要插入分卷标题
                need_volume_header = True
                for line in new_lines:
                    if line.strip() == f"## 第{volume_no}卷":
                        need_volume_header = False
                        break
                
                if need_volume_header and insert_pos < len(new_lines):
                    new_lines.insert(insert_pos, f"## 第{volume_no}卷")
                    insert_pos += 1
            
            new_lines.insert(insert_pos, new_entry)
        else:
            # 没有分卷号，插入到末尾（在所有章节条目之后）
            insert_pos = len(new_lines)
            for i, line in enumerate(new_lines):
                if line.strip().startswith('-') and '章' in line:
                    insert_pos = i + 1
            new_lines.insert(insert_pos, new_entry)
    
    # 重新组织内容（按分卷分组）
    organized_lines = []
    current_volume = None
    has_volume_markers = any(re.search(r'\[卷(\d+)\]', line) for line in new_lines if line.strip().startswith('-'))
    
    # 保留标题行
    for line in new_lines:
        if line.strip().startswith('#'):
            # 跳过已有的分卷标题（稍后会重新生成）
            if not re.match(r'## 第\d+卷', line.strip()):
                organized_lines.append(line)
    
    if has_volume_markers:
        # 按分卷分组
        chapters_by_volume = {}
        ungrouped_chapters = []
        
        for line in new_lines:
            if line.strip().startswith('-'):
                volume_match = re.search(r'\[卷(\d+)\]', line)
                if volume_match:
                    vol = int(volume_match.group(1))
                    if vol not in chapters_by_volume:
                        chapters_by_volume[vol] = []
                    chapters_by_volume[vol].append(line)
                else:
                    ungrouped_chapters.append(line)
        
        # 按分卷号排序输出
        for vol in sorted(chapters_by_volume.keys()):
            organized_lines.append(f"## 第{vol}卷")
            organized_lines.extend(chapters_by_volume[vol])
            organized_lines.append('')
        
        # 添加未分组的章节
        if ungrouped_chapters:
            organized_lines.extend(ungrouped_chapters)
    else:
        # 没有分卷标记，保持原样
        for line in new_lines:
            if not line.strip().startswith('#'):
                organized_lines.append(line)
    
    content = '\n'.join(organized_lines)
    
    index_file.write_text(content, encoding="utf-8")

