# 뉴스 데이터 수집

import requests  # HTTP 요청을 보내기 위한 requests 라이브러리 가져오기
from config import NEWS_API_KEY  # NewsAPI의 API 키 가져오기

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"  # NewsAPI의 엔드포인트 URL

def fetch_news(query: str = "education", source: str = "bbc-news"):
    """NewsAPI에서 뉴스 가져오기"""
    params = {
        "q": query,  # 검색할 키워드
        "sources": source,  # 뉴스 출처
        "apiKey": NEWS_API_KEY  # API 키
    }
    response = requests.get(NEWS_API_URL, params=params)  # GET 요청을 보내 뉴스 데이터 가져오기
    if response.status_code == 200:  # 요청이 성공한 경우
        return response.json()["articles"]  # 응답에서 뉴스 기사 목록 반환
    return []  # 요청이 실패한 경우 빈 리스트 반환