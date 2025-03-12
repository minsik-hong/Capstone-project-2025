import openai
import numpy as np
from services.vector_db import VectorDB
from services.news_fetcher import fetch_news
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
vector_db = VectorDB()

def search_news(query: str):
    """벡터DB에서 관련 뉴스 검색"""
    query_vector = np.random.rand(512).astype(np.float32)  # ✅ 실제로는 임베딩 필요
    related_news_indices = vector_db.search(query_vector, top_k=3)

    news_results = []
    for idx in related_news_indices:
        news_results.append(fetch_news()[idx])  # ✅ 예제 코드, 실제 뉴스 가져오기 필요

    return news_results

def chatbot_response(user_query: str):
    """사용자 질문을 받아 RAG 기반 뉴스 답변 생성"""
    related_news = search_news(user_query)

    context = "\n".join([f"- {news['title']}: {news['summary']}" for news in related_news])

    prompt = f"""
    The user asked: "{user_query}"
    Here are some relevant news articles:
    {context}

    Based on these articles, provide a concise and informative response.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that answers questions based on real news articles."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]
