import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import weaviate

from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

# ========== 환경 변수 설정 ==========
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))

print(f"Connecting to Weaviate at {WEAVIATE_HOST}:{WEAVIATE_PORT}")

connection_params = ConnectionParams.from_params(
    http_host=WEAVIATE_HOST,
    http_port=WEAVIATE_PORT,
    http_secure=False,
    grpc_host=WEAVIATE_HOST,
    grpc_port=WEAVIATE_GRPC_PORT,
    grpc_secure=False
)

client = weaviate.WeaviateClient(connection_params=connection_params)
try:
    client.connect()
    print(f"Successfully connected to Weaviate at {WEAVIATE_HOST}:{WEAVIATE_PORT}")
except Exception as e:
    print(f"Failed to connect to Weaviate at {WEAVIATE_HOST}:{WEAVIATE_PORT}")
    print(f"Error: {e}")
    print("\nTip: If running locally, make sure:")
    print("  1. Weaviate is running (docker-compose up weaviate)")
    print("  2. WEAVIATE_HOST is set to 'localhost' in .env file")
    print("  3. If using Docker, set WEAVIATE_HOST to 'weaviate'")
    raise

# Check if URL exists in Weaviate (중복 체크)
def is_url_in_weaviate(url, index_name):
    try:
        from weaviate.classes.query import Filter
        
        collection = client.collections.get(index_name)
        result = collection.query.fetch_objects(
            filters=Filter.by_property("url").equal(url),
            limit=1
        )
        return len(result.objects) > 0
    except Exception as e:
        # 컬렉션이 없거나 에러 발생 시 중복 아님으로 처리
        if "does not exist" in str(e).lower():
            return False
        print("Weaviate 중복 확인 실패:", e)
        return False


# 기사 유효성 필터
def is_valid_news_article(article, source: str = "") -> bool:
    url = article.get("url", "").lower()
    title = article.get("title", "").strip().lower()
    description = article.get("description", "") or ""
    
    # BBC는 articles 경로 확인, CNN은 다른 URL 구조 허용
    if source == "bbc-news":
        if "articles" not in url:
            return False
    elif source == "cnn":
        # CNN URL 패턴: cnn.com/2025/... 형식
        if "cnn.com" not in url:
            return False
    
    # 제외할 키워드 (뉴스 요약, 오디오 등)
    repetitive_keywords = [
        "five minute news bulletin", "bbc world service", "news summary",
        "news update", "listen to the latest news", "bulletin",
        "audio", "programme", "world service", 'bitesize', 'news in brief',
    ]
    if any(kw in title for kw in repetitive_keywords):
        return False
    if any(kw in description.lower() for kw in repetitive_keywords):
        return False
    return True

# 본문 스크래핑
def scrape_full_content(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            return ' '.join(p.get_text() for p in paragraphs)
    except Exception as e:
        print(f" 스크래핑 실패: {url} ({str(e)})")
    return None

# 뉴스 수집
def fetch_news_from_to(query: str, start_date: str, end_date: str, source: str):
    url = "https://newsapi.org/v2/everything"
    all_results = []
    api_call_count = 0

    start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    delta = timedelta(days=5)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
    if start_dt < cutoff_date:
        print(f" 시작일 {start_date}은 무료 플랜 범위를 초과함.")
        return []

    while start_dt < end_dt:
        from_str = start_dt.strftime("%Y-%m-%d")
        to_dt = min(start_dt + delta, end_dt)
        to_str = to_dt.strftime("%Y-%m-%d")
        print(f"\n 수집 중: {from_str} ~ {to_str}")

        params = {
            "q": query,
            "sources": source,
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
            print(f" API 실패: {response.text}")
            start_dt = to_dt
            continue

        articles = response.json().get("articles", [])
        if not articles:
            start_dt = to_dt
            continue

        for article in articles:
            if not is_valid_news_article(article, source):
                continue

            full_content = scrape_full_content(article["url"])
            if not full_content or len(full_content.strip()) < 300:
                continue

            all_results.append({
                "title": article.get("title", "").strip(),
                "author": article.get("author", ""),
                "content": full_content,
                "description": article.get("description", ""),
                "url": article.get("url"),
                "urlToImage": article.get("urlToImage"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "publishedAt": article.get("publishedAt", datetime.now(timezone.utc).isoformat())
            })

        start_dt = to_dt

    print(f"\n 총 API 호출 횟수: {api_call_count}회")
    print(f" 최종 수집된 유효 기사 수: {len(all_results)}개")
    return all_results

# 저장 및 벡터화
def save_and_vectorize_langchain(articles, source_name, start_date, end_date):
    save_dir = "data/news_articles"
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{source_name}_{start_date}~{end_date}.json"
    filepath = os.path.join(save_dir, filename)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing_articles = json.load(f)
    else:
        existing_articles = []

    existing_urls = {a["url"] for a in existing_articles}
    new_articles = [a for a in articles if a["url"] not in existing_urls]
    combined = existing_articles + new_articles

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)

    print(f" 저장 완료: {filename} — 새 기사 {len(new_articles)}개 추가됨")

    print(f" LangChain 벡터화 시작: {source_name}")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    docs = [
        Document(
            page_content=article["content"],
            metadata={
                "title": article["title"],
                "author": article["author"],
                "description": article["description"],
                "url": article["url"],
                "urlToImage": article["urlToImage"],
                "source": article["source"],
                "publishedAt": article["publishedAt"]
            }
        )
        for article in new_articles
    ]

    # Weaviate 중복 확인 후 없는 것만 넣기
    docs_to_add = []
    duplicate_count = 0
    index_name = f"news_{source_name}".lower()

    for doc in docs:
        url = doc.metadata["url"]
        if not is_url_in_weaviate(url, index_name):
            docs_to_add.append(doc)
        else:
            duplicate_count += 1

    if docs_to_add:
        vector_store = WeaviateVectorStore.from_documents(
            documents=docs_to_add,
            embedding=embedding_model,
            client=client,
            index_name=index_name,
            text_key="content"
        )
        print(f" LangChain 벡터화 완료: {source_name}, 총 {len(docs_to_add)}개 추가, 중복 제외 {duplicate_count}개")
    else:
        print(f" LangChain 벡터화 완료: {source_name}, 추가 없음, 중복 제외 {duplicate_count}개")

# 저장된 기사 파일 불러오기 및 벡터화
def load_and_vectorize_from_file(source_name, start_date, end_date):
    filepath = os.path.join("data/news_articles", f"{source_name}_{start_date}~{end_date}.json")
    if not os.path.exists(filepath):
        print(f" 파일이 존재하지 않습니다: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f" LangChain 벡터화 시작: {source_name} ({len(articles)}개)")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    docs = [
        Document(
            page_content=article["content"],
            metadata={
                "title": article["title"],
                "author": article.get("author", ""),
                "description": article["description"],
                "url": article["url"],
                "urlToImage": article.get("urlToImage", ""),
                "source": article["source"],
                "publishedAt": article["publishedAt"]
            }
        )
        for article in articles
    ]

    vector_store = WeaviateVectorStore.from_documents(
        documents=docs,
        embedding=embedding_model,
        client=client,
        index_name=f"news_{source_name}".lower(),
        text_key="content"
    )

    vector_store.add_documents(docs)

# 실행
if __name__ == "__main__":
    start_date = "2025-11-04"
    end_date = "2025-12-01"
    sources = [
        {"api_name": "bbc-news", "name": "bbc"},
        {"api_name": "cnn", "name": "cnn"}
    ]

    for source in sources:
        print(f"\n {source['name'].upper()} 뉴스 수집 중...")
        articles = fetch_news_from_to(
            query="",
            start_date=start_date,
            end_date=end_date,
            source=source["api_name"]
        )
        save_and_vectorize_langchain(
            articles,
            source_name=source["name"],
            start_date=start_date,
            end_date=end_date
        )

    for source in sources:
        print(f"\n {source['name'].upper()} 벡터화 실행 중...")
        load_and_vectorize_from_file(
            source_name=source["name"],
            start_date=start_date,
            end_date=end_date
        )

    client.close()
