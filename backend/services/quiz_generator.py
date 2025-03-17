import openai  # OpenAI API를 사용하기 위한 라이브러리 가져오기
from config import OPENAI_API_KEY  # OpenAI API 키 가져오기

openai.api_key = OPENAI_API_KEY  # OpenAI API 키 설정

def generate_quiz(news_text: str):
    """GPT-4를 사용하여 뉴스 내용을 기반으로 퀴즈 생성"""
    prompt = f"""
    Create a multiple-choice quiz based on the following news article. 
    Provide three options and indicate the correct answer.

    News Article: {news_text}
    """  # 뉴스 내용을 기반으로 퀴즈를 생성하기 위한 프롬프트 정의

    response = openai.ChatCompletion.create(
        model="gpt-4",  # GPT-4 모델 사용
        messages=[
            {"role": "system", "content": "You are an AI that generates quizzes from news articles."},  # 시스템 역할 정의
            {"role": "user", "content": prompt}  # 사용자 프롬프트 전달
        ]
    )

    return response["choices"][0]["message"]["content"]  # 생성된 퀴즈 내용을 반환