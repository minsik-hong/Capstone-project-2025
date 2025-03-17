# AI 뉴스 요약

import openai  # OpenAI API를 사용하기 위한 라이브러리 가져오기
from config import OPENAI_API_KEY  # OpenAI API 키 가져오기

openai.api_key = OPENAI_API_KEY  # OpenAI API 키 설정

def summarize_text(text: str) -> str:
    """GPT를 이용한 뉴스 요약"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # GPT-4 모델 사용
        messages=[
            {"role": "system", "content": "Summarize this news article."},  # 시스템 역할 정의
            {"role": "user", "content": text}  # 사용자로부터 입력받은 뉴스 본문 전달
        ]
    )
    return response["choices"][0]["message"]["content"]  # 요약된 뉴스 내용을 반환