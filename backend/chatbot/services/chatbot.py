import openai
from backend.db_builder.vector_db import VectorDB  # 벡터DB 관련 서비스 가져오기
from backend.config import OPENAI_API_KEY  # OpenAI API 키 가져오기

openai.api_key = OPENAI_API_KEY  # OpenAI API 키 설정
vector_db = VectorDB()  # 벡터DB 인스턴스 생성

def search_news(query: str):
    """벡터DB에서 관련 뉴스 검색"""
    query_vector = vector_db.get_embedding(query)  # 사용자 질문을 벡터로 변환
    related_news_indices = vector_db.search(query_vector, top_k=3)  # 벡터DB에서 상위 3개의 관련 뉴스 검색

    news_results = []
    for idx in related_news_indices:  # 검색된 뉴스 인덱스를 순회
        news_entry = vector_db.get_metadata(idx)  # 벡터 DB에서 메타데이터 가져오기
        news_results.append(news_entry)

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

    try:
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
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")  # 에러 메시지 출력
        return "죄송합니다. 현재 답변을 생성할 수 없습니다."