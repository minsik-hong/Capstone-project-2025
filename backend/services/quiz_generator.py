import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_quiz(news_text: str):
    """GPT-4를 사용하여 뉴스 내용을 기반으로 퀴즈 생성"""
    prompt = f"""
    Create a multiple-choice quiz based on the following news article. 
    Provide three options and indicate the correct answer.

    News Article: {news_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates quizzes from news articles."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]
