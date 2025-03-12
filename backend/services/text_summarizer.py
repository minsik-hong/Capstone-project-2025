# AI 뉴스 요약

import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_text(text: str) -> str:
    """GPT를 이용한 뉴스 요약"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize this news article."},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]
