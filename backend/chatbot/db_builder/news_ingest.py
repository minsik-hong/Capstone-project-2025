import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import openai
import chromadb
from chromadb.config import Settings
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

# ====================== 메인 수집 파이프라인 ===========================
def fetch_and_process_news(topics, output_file=NEWS_JSON_FILE):
    all_articles = []

    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            all_articles = json.load(f)
    existing_urls = {a["url"] for a in all_articles}

    for topic in topics:
        print(f"🔍 '{topic}' 주제 뉴스 수집 중...")
        new_articles = fetch_news(query=topic)
        new_articles = [a for a in new_articles if a["url"] not in existing_urls]
        print(f"✅ 새 뉴스 {len(new_articles)}개 수집됨")

        all_articles.extend(new_articles)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)
    return all_articles

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
    topics = ["technology", "education", "health", "science"]
    fetch_and_process_news(topics)
    build_vector_db_from_news()
    print("✅ 뉴스 수집 + 임베딩 + 벡터 DB 저장 완료!")
