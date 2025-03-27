import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import openai
import chromadb
from chromadb.config import Settings
from datetime import datetime, timedelta
from langchain_community.document_loaders import JSONLoader

load_dotenv()

# ====================== 설정 ===========================
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = True
VECTOR_DB_DIR = "data/vector_db"
NEWS_JSON_FILE = "data/news_articles.json"
hf_model = SentenceTransformer('all-MiniLM-L6-v2')
openai.api_key = OPENAI_API_KEY

# ====================== 뉴스 수집 ===========================
def fetch_news(query: str, source: str = "bbc-news"):
    """NewsAPI에서 뉴스 가져오기"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sources": source,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ 뉴스 API 요청 실패: {response.text}")
        return []

    articles = response.json().get("articles", [])
    results = []
    for article in articles:
        if not article.get("url"):
            continue
        full_content = scrape_full_content(article["url"])
        results.append({
            "title": article.get("title", "No Title"),
            "content": full_content or article.get("content", "No Content"),
            "description": article.get("description", "No Description"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name", "Unknown Source")
        })
    return results

def scrape_full_content(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            return ' '.join(p.get_text() for p in paragraphs)
    except Exception as e:
        print(f"⚠️ 스크래핑 실패: {url} ({str(e)})")
    return None

# ====================== 임베딩 생성 ===========================
def get_embedding(text: str):
    """텍스트 임베딩 벡터 생성"""
    if USE_OPENAI:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]
    else:
        return hf_model.encode(text)

# ====================== 벡터 DB 저장 ===========================
class VectorDB:
    def __init__(self, collection_name="news_vectors"):
        self.client = chromadb.Client(Settings(persist_directory=VECTOR_DB_DIR))
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_vector(self, vector, metadata):
        existing = self.collection.query(where={"url": metadata["url"]}, n_results=1)
        if existing["ids"]:
            print(f"⚠️ 이미 존재하는 URL: {metadata['url']}")
            return
        self.collection.add(embeddings=[vector], metadatas=[metadata])

    def search(self, query_vector, top_k=5):
        return self.collection.query(query_embeddings=[query_vector], n_results=top_k)


# ====================== 반복 뉴스 필터링 함수 ===========================
def is_repetitive_bbc_news(title: str, description: str = "") -> bool:
    title = title.strip().lower()
    repetitive_titles = [
        "the latest five minute news bulletin from bbc world service.",
        "news briefing",
        "bbc world news bulletin",
    ]

    repetitive_keywords = [
        "five minute news bulletin",
        "bbc world service",
        "news summary",
        "news update",
        "listen to the latest news",
    ]

    if title in repetitive_titles:
        return True

    for keyword in repetitive_keywords:
        if keyword in title or keyword in description.lower():
            return True

    return False


# ====================== 메인 수집 파이프라인 ===========================
def fetch_bbc_news_from_to(query: str, start_date: str, end_date: str):
    """
    무료 NewsAPI 조건에 맞춰 BBC 뉴스 수집
    - page=1만 허용 (100개까지)
    - 반복성 뉴스 필터링
    """
    url = "https://newsapi.org/v2/everything"
    all_results = []
    api_call_count = 0

    # 날짜 파싱
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=5)  # 날짜를 더 세분화해서 잘 가져오기

    # 무료 플랜에서는 현재 기준 30일 이내만 가능
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    if start_dt < cutoff_date:
        print(f"⚠️ 시작일 {start_date}은 무료 플랜 범위를 초과함. {cutoff_date.date()} 이후로 설정하세요.")
        return []

    while start_dt < end_dt:
        from_str = start_dt.strftime("%Y-%m-%d")
        to_dt = min(start_dt + delta, end_dt)
        to_str = to_dt.strftime("%Y-%m-%d")
        print(f"\n📅 수집 중: {from_str} ~ {to_str}")

        # 무료 플랜은 page=1까지만 허용
        params = {
            "q": query,
            "sources": "bbc-news",
            "from": from_str,
            "to": to_str,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 100,
            "page": 1,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params)
        api_call_count += 1

        if response.status_code != 200:
            print(f"❌ API 실패: {response.text}")
            start_dt = to_dt
            continue

        articles = response.json().get("articles", [])
        if not articles:
            print(f"❗ 기사 없음 (page 1)")
            start_dt = to_dt
            continue

        print(f"📄 {len(articles)}개 기사 수집됨")

        repetitive_news_count = 0  # ⏱️ 반복 뉴스 개수 카운터
        for article in articles:
            title = article.get("title", "").strip()
            description = article.get("description", "")

            # ✅ 반복성 뉴스 필터링
            if is_repetitive_bbc_news(title, description):
                repetitive_news_count += 1
                continue
            
            full_content = scrape_full_content(article["url"])
            # ✅ 유효 뉴스 저장
            all_results.append({
                "title": article.get("title", "No Title"),
                "content": full_content,
                "description": article.get("description", "No Description"),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name", "Unknown Source")
            })

        # 🔚 반복문 끝난 후 출력
        print(f"\n🔁 제외된 반복 뉴스 개수: {repetitive_news_count}개")
        start_dt = to_dt

    print(f"\n📡 총 API 호출 횟수: {api_call_count}회")
    print(f"📰 최종 수집된 유효 기사 수: {len(all_results)}개")
    return all_results



def build_vector_db_from_news(news_file=NEWS_JSON_FILE):
    loader = JSONLoader(file_path=news_file, jq_schema=".", text_content=False)
    documents = loader.load()
    print(f"🧠 총 {len(documents)}개 문서 로드됨")

    vdb = VectorDB()
    for doc in documents:
        content = doc.metadata.get("content", "")
        if not content: continue
        vector = get_embedding(content)
        vdb.add_vector(vector, metadata=doc.metadata)

# ====================== 실행 ===========================
if __name__ == "__main__":
    print("📰 BBC 뉴스 수집 시작...")

    articles = fetch_bbc_news_from_to(
        query="",
        start_date="2025-03-01",  
        end_date="2025-03-27"
    )

    # ✅ 디렉토리 생성
    os.makedirs(os.path.dirname(NEWS_JSON_FILE), exist_ok=True)

    # ✅ JSON 저장
    with open(NEWS_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    # ✅ 벡터 DB 구축
    build_vector_db_from_news()

    print("✅ BBC 뉴스 수집 + 임베딩 + 벡터 DB 저장 완료!")
