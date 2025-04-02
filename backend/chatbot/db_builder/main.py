import sys
import os
import json

# 프로젝트 루트 경로를 PYTHONPATH에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(project_root)

from backend.chatbot.db_builder.news_fetcher import fetch_news
from backend.chatbot.db_builder.embedding import get_embedding
from backend.chatbot.db_builder.vector_db import VectorDB
from langchain_community.document_loaders import JSONLoader  # 경로 업데이트

def fetch_and_save_news(query, source, output_file):
    articles = fetch_news(query=query, source=source)
    print("fetch_news 반환값:", articles)  # fetch_news 함수의 반환값 출력
    if not articles:
        print("⚠️ 뉴스 데이터를 가져오지 못했습니다. API 키와 요청 매개변수를 확인하세요.")
        return
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"{output_file}에 데이터 저장 완료.")  # 저장 완료 메시지 출력

def main():
    topics = ["technology", "education", "health", "science"]  # 여러 주제 정의
    output_file = "backend/data/news_articles.json"

    for topic in topics:
        print(f"🔍 '{topic}' 주제의 뉴스를 가져오는 중...")
        fetch_and_save_news(query=topic, source="bbc-news", output_file=output_file)

    # LangChain Document Loader로 로드
    loader = JSONLoader(file_path=output_file, jq_schema=".", text_content=False)
    documents = loader.load()
    
    print(f"총 {len(documents)}개의 뉴스 문서가 로드되었습니다.")
    
    # # JSON 파일 내용 출력
    # with open(output_file, "r") as f:
    #     data = json.load(f)
    #     print("저장된 뉴스 데이터:", json.dumps(data, indent=2, ensure_ascii=False))
    #     if not data:
    #         print("⚠️ JSON 파일이 비어 있습니다. fetch_news 함수의 반환값을 확인하세요.")

if __name__ == "__main__":
    main()