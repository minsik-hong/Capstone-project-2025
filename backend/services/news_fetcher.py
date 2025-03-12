# 뉴스 데이터 수집

import requests
from config import NEWS_API_KEY

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(query: str = "education", source: str = "bbc-news"):
    """NewsAPI에서 뉴스 가져오기"""
    params = {
        "q": query,
        "sources": source,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()["articles"]
    return []
