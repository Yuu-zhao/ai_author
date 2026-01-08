"""UI工具函数模块"""
from pathlib import Path


def get_files(directory: Path, pattern: str = "*.md"):
    """获取目录下的所有文件"""
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    return sorted(directory.glob(pattern), key=lambda x: x.name)


def save_file(path: Path, content: str):
    """保存文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def delete_file(path: Path):
    """删除文件"""
    if path.exists():
        path.unlink()
        return True
    return False

