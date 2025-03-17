# 뉴스 API 엔드포인트

from fastapi import APIRouter, Depends  # FastAPI 라우터와 의존성 주입을 위한 Depends 가져오기
from services.news_fetcher import fetch_news  # 뉴스 데이터를 가져오는 서비스 함수 가져오기
from services.text_summarizer import summarize_text  # 텍스트 요약을 위한 서비스 함수 가져오기
from db import get_db  # 데이터베이스 세션을 가져오는 함수 가져오기
from sqlalchemy.orm import Session  # SQLAlchemy 세션 클래스 가져오기
from models.news import NewsArticle  # 뉴스 기사 모델 가져오기

router = APIRouter()  # 새로운 라우터 인스턴스 생성

@router.get("/")  # HTTP GET 요청을 처리하는 엔드포인트 정의
def get_news(query: str = "technology", source: str = "bbc-news", db: Session = Depends(get_db)):
    """뉴스 검색 & 요약"""
    articles = fetch_news(query, source)  # 뉴스 데이터를 가져오기
    result = []  # 결과를 저장할 리스트 초기화

    for article in articles:  # 가져온 뉴스 기사들을 순회
        summary = summarize_text(article["content"])  # 뉴스 본문을 요약
        news_entry = NewsArticle(  # 뉴스 기사 객체 생성
            title=article["title"],  # 뉴스 제목
            content=article["content"],  # 뉴스 본문
            summary=summary,  # 요약된 내용
            url=article["url"],  # 뉴스 원문 URL
            source=article["source"]["name"]  # 뉴스 출처
        )
        db.add(news_entry)  # 데이터베이스에 뉴스 기사 추가
        db.commit()  # 변경 사항 커밋
        db.refresh(news_entry)  # 데이터베이스에서 새로 추가된 객체를 갱신

        result.append({  # 결과 리스트에 추가
            "title": article["title"],  # 뉴스 제목
            "summary": summary,  # 요약된 내용
            "url": article["url"],  # 뉴스 원문 URL
            "source": article["source"]["name"]  # 뉴스 출처
        })

    return result  # 결과 반환