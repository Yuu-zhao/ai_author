from openai import OpenAI
from config import MODEL_NAME, OPENAI_API_KEY

# 延迟初始化客户端，避免模块导入时的错误
_client = None

def get_client():
    """获取 OpenAI 客户端（延迟初始化）"""
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未设置，请在 .env 文件中配置")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client

def generate_chapter(prompt):
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是严谨、克制的小说协作者"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

