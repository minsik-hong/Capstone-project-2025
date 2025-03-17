# 뉴스 데이터 모델 

from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

# 뉴스 기사 모델 정의
class NewsArticle(Base):
    __tablename__ = "news_articles"  # 데이터베이스 테이블 이름

    id = Column(Integer, primary_key=True, index=True)  # 기본 키
    title = Column(String, index=True)  # 뉴스 제목 (인덱스 생성)
    content = Column(String)  # 뉴스 본문 내용
    summary = Column(String)  # 뉴스 요약
    url = Column(String)  # 뉴스 원문 URL
    source = Column(String)  # 뉴스 출처
    published_at = Column(DateTime, default=datetime.utcnow)  # 뉴스 게시 날짜 (기본값: 현재 시간)