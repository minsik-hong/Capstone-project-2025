# 뉴스 데이터 모델 

from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    summary = Column(String)
    url = Column(String)
    source = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)
