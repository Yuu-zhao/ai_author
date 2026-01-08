import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "灵气靖朝录"
MODEL_NAME = "gpt-4.1"

DATA_PATH = "data"
PROMPT_PATH = "prompts/chapter_prompt.txt"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

