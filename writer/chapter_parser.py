"""章节解析工具 - 用于解析章节目录索引"""
import re
from pathlib import Path
from typing import List, Dict, Optional

def parse_chapter_index() -> Dict[str, List[Dict]]:
    """
    解析章节目录索引，返回按分卷组织的章节信息
    
    Returns:
        {
            "volumes": {
                "1": [
                    {"chapter_no": "第1章", "summary": "...", "volume_no": 1},
                    ...
                ],
                ...
            },
            "ungrouped": [
                {"chapter_no": "第X章", "summary": "...", "volume_no": None},
                ...
            ]
        }
    """
    index_file = Path("data/plot/chapter_index.md")
    if not index_file.exists():
        return {"volumes": {}, "ungrouped": []}
    
    content = index_file.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    result = {"volumes": {}, "ungrouped": []}
    current_volume = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否是分卷标题
        volume_match = re.match(r'##\s*第(\d+)卷', line)
        if volume_match:
            current_volume = int(volume_match.group(1))
            if str(current_volume) not in result["volumes"]:
                result["volumes"][str(current_volume)] = []
            continue
        
        # 检查是否是章节条目
        chapter_match = re.match(r'-\s*(.+?)(?:\s*\[卷(\d+)\])?\s*[：:]\s*(.+)', line)
        if chapter_match:
            chapter_no = chapter_match.group(1).strip()
            volume_no = int(chapter_match.group(2)) if chapter_match.group(2) else current_volume
            summary = chapter_match.group(3).strip()
            
            chapter_info = {
                "chapter_no": chapter_no,
                "summary": summary,
                "volume_no": volume_no
            }
            
            if volume_no:
                vol_str = str(volume_no)
                if vol_str not in result["volumes"]:
                    result["volumes"][vol_str] = []
                result["volumes"][vol_str].append(chapter_info)
            else:
                result["ungrouped"].append(chapter_info)
    
    return result

def get_chapter_file_path(chapter_no: str) -> Optional[Path]:
    """获取章节文件路径"""
    chapter_file = Path(f"data/chapters/{chapter_no}.md")
    if chapter_file.exists():
        return chapter_file
    return None

