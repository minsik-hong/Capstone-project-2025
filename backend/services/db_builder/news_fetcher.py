import os
import requests
import json
from bs4 import BeautifulSoup  # 웹 스크래핑을 위한 라이브러리 추가
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader  # 업데이트된 import 경로

# .env 파일 로드
load_dotenv()

NEWS_API_URL = "https://newsapi.org/v2/everything"  # 올바른 엔드포인트로 수정
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    print("⚠️ NEWS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")  # 디버깅 메시지 추가

def fetch_news(query: str = "education", source: str = "bbc-news"):
    """NewsAPI에서 뉴스 가져오기"""
    params = {
        "q": query,
        "sources": source,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    print("API 요청 URL:", response.url)  # 요청 URL 출력
    print("응답 상태 코드:", response.status_code)  # HTTP 상태 코드 출력
    
    if response.status_code == 200:
        try:
            articles = response.json().get("articles", [])
            print("API 응답 데이터:", json.dumps(response.json(), indent=2, ensure_ascii=False))  # 응답 데이터 출력
            # LangChain Document Loader로 변환
            documents = []
            for article in articles:
                if article.get("content"):
                    full_content = scrape_full_content(article.get("url"))  # 웹 스크래핑으로 content 확장
                    documents.append({
                        "title": article.get("title", "No Title"),
                        "content": full_content or article.get("content", "No Content"),
                        "description": article.get("description", "No Description"),
                        "url": article.get("url", "No URL"),
                        "source": article.get("source", {}).get("name", "Unknown Source")
                    })
            return documents
        except Exception as e:
            print("⚠️ 응답 데이터 처리 중 오류 발생:", str(e))
            return []
    else:
        print("⚠️ API 요청 실패:", response.text)  # 실패 메시지 출력
        return []

def scrape_full_content(url: str) -> str:
    """웹 스크래핑을 통해 전체 기사 내용 가져오기"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')  # <p> 태그로 기사 내용 추출
            full_content = ' '.join([p.get_text() for p in paragraphs])
            return full_content
        else:
            print(f"⚠️ 스크래핑 실패: {url} (상태 코드: {response.status_code})")
            return None
    except Exception as e:
        print(f"⚠️ 스크래핑 중 오류 발생: {str(e)}")
        return None

def fetch_and_save_news(query: str = "education", source: str = "bbc-news", output_file: str = "data/news_articles.json"):
    """뉴스 데이터를 가져와 JSON 파일로 저장"""
    # 기존 데이터 로드
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            existing_articles = json.load(f)
    else:
        existing_articles = []

    # 기존 URL 목록 생성
    existing_urls = {article["url"] for article in existing_articles}

    # 새 기사 가져오기
    articles = fetch_news(query, source)

    # 중복 제거
    new_articles = [article for article in articles if article["url"] not in existing_urls]

    # 병합 및 저장
    all_articles = existing_articles + new_articles
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)
    print(f"뉴스 데이터가 {output_file}에 저장되었습니다. (새로운 기사 {len(new_articles)}개 추가)")