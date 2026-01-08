import sys
from main import run_chapter

chapter_no = sys.argv[1]
goal = sys.argv[2]

filename = f"data/chapters/{chapter_no}.md"

run_chapter(chapter_no, goal, filename)

