# 뉴스 API 엔드포인트

from fastapi import APIRouter, Depends
from services.news_fetcher import fetch_news
from services.text_summarizer import summarize_text
from db import get_db
from sqlalchemy.orm import Session
from models.news import NewsArticle

router = APIRouter()

@router.get("/")
def get_news(query: str = "technology", source: str = "bbc-news", db: Session = Depends(get_db)):
    """뉴스 검색 & 요약"""
    articles = fetch_news(query, source)
    result = []

    for article in articles:
        summary = summarize_text(article["content"])
        news_entry = NewsArticle(
            title=article["title"],
            content=article["content"],
            summary=summary,
            url=article["url"],
            source=article["source"]["name"]
        )
        db.add(news_entry)
        db.commit()
        db.refresh(news_entry)
        
        result.append({
            "title": article["title"],
            "summary": summary,
            "url": article["url"],
            "source": article["source"]["name"]
        })

    return result
