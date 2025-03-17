import openai
import numpy as np
from services.vector_db import VectorDB  # 벡터DB 관련 서비스 가져오기
from services.news_fetcher import fetch_news  # 뉴스 데이터를 가져오는 서비스 가져오기
from config import OPENAI_API_KEY  # OpenAI API 키 가져오기

openai.api_key = OPENAI_API_KEY  # OpenAI API 키 설정
vector_db = VectorDB()  # 벡터DB 인스턴스 생성

def search_news(query: str):
    """벡터DB에서 관련 뉴스 검색"""
    query_vector = np.random.rand(512).astype(np.float32)  # ✅ 실제로는 임베딩 필요 (현재는 임의의 벡터 사용)
    related_news_indices = vector_db.search(query_vector, top_k=3)  # 벡터DB에서 상위 3개의 관련 뉴스 검색

    news_results = []
    for idx in related_news_indices:  # 검색된 뉴스 인덱스를 순회
        news_results.append(fetch_news()[idx])  # ✅ 예제 코드, 실제 뉴스 가져오기 필요

    return news_results  # 관련 뉴스 반환

def chatbot_response(user_query: str):
    """사용자 질문을 받아 RAG 기반 뉴스 답변 생성"""
    related_news = search_news(user_query)  # 사용자 질문과 관련된 뉴스 검색

    # 관련 뉴스의 제목과 요약을 컨텍스트로 생성
    context = "\n".join([f"- {news['title']}: {news['summary']}" for news in related_news])

    # 사용자 질문과 관련 뉴스 컨텍스트를 포함한 프롬프트 생성
    prompt = f"""
    The user asked: "{user_query}"
    Here are some relevant news articles:
    {context}

    Based on these articles, provide a concise and informative response.
    """

    # OpenAI GPT-4 모델을 사용하여 답변 생성
    response = openai.ChatCompletion.create(
        model="gpt-4",  # GPT-4 모델 사용
        messages=[
            {"role": "system", "content": "You are an AI assistant that answers questions based on real news articles."},  # 시스템 역할 정의
            {"role": "user", "content": prompt}  # 사용자 프롬프트 전달
        ]
    )

    # 생성된 답변 내용 반환
    return response["choices"][0]["message"]["content"]