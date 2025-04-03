import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Weaviate 연결 설정
connection_params = ConnectionParams.from_params(
    http_host="localhost",
    http_port=8080,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False
)
client = WeaviateClient(connection_params=connection_params)
client.connect()

# 중복 뉴스 필터
def is_repetitive_news(title: str, description: str = "") -> bool:
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

# 기사 본문 스크래핑
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
        print(f"⚠️ 시작일 {start_date}은 무료 플랜 범위를 초과함. {cutoff_date.date()} 이후로 설정하세요.")
        return []

    while start_dt < end_dt:
        from_str = start_dt.strftime("%Y-%m-%d")
        to_dt = min(start_dt + delta, end_dt)
        to_str = to_dt.strftime("%Y-%m-%d")
        print(f"\n📅 수집 중: {from_str} ~ {to_str}")

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
            print(f"❌ API 실패: {response.text}")
            start_dt = to_dt
            continue

        articles = response.json().get("articles", [])
        if not articles:
            start_dt = to_dt
            continue

        for article in articles:
            title = article.get("title", "").strip()
            description = article.get("description", "")
            if is_repetitive_news(title, description):
                continue
            full_content = scrape_full_content(article["url"])
            if not full_content or len(full_content.strip()) < 300:
                continue
            all_results.append({
                "title": title,
                "content": full_content,
                "description": description,
                "url": article.get("url"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "publishedAt": article.get("publishedAt", datetime.now(timezone.utc).isoformat())
            })
        start_dt = to_dt

    print(f"\n📡 총 API 호출 횟수: {api_call_count}회")
    print(f"📰 최종 수집된 유효 기사 수: {len(all_results)}개")
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

    print(f"💾 저장 완료: {filename} — 새 기사 {len(new_articles)}개 추가됨")

    print(f"⚙️ LangChain 벡터화 시작: {source_name}")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    docs = [
        Document(
            page_content=article["content"],
            metadata={k: article[k] for k in article if k != "content"}
        )
        for article in new_articles
        if article.get("content", "").strip()
    ]

    vector_store = WeaviateVectorStore.from_documents(
        documents=docs,
        embedding=embedding_model,
        client=client,
        index_name=f"news_{source_name}".lower(),
        text_key="content"
    )

    print(f"✅ LangChain 벡터화 완료: {source_name}, 총 {len(new_articles)}개 추가")

# 저장된 기사 파일 불러오기 및 벡터화(api 호출 없이 기존 파일을 벡터로)
def load_and_vectorize_from_file(source_name, start_date, end_date):
    filepath = os.path.join("backend/data/news_articles", f"{source_name}_{start_date}~{end_date}.json")
    if not os.path.exists(filepath):
        print(f"❌ 파일이 존재하지 않습니다: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"⚙️ LangChain 벡터화 시작: {source_name} ({len(articles)}개)")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    docs = [
        Document(
            page_content=article["content"],
            metadata={k: article[k] for k in article if k != "content"}
        )
        for article in articles
        if article.get("content", "").strip()
    ]

    vector_store = WeaviateVectorStore.from_documents(
        documents=docs,
        embedding=embedding_model,
        client=client,
        index_name=f"news_{source_name}".lower(),
        text_key="text"
    )



# 실행
if __name__ == "__main__":
    start_date = "2025-03-06"
    end_date = "2025-03-27"
    sources = [
        {"api_name": "bbc-news", "name": "bbc"},
        {"api_name": "cnn", "name": "cnn"}
    ]

    # api 호출 벡터화 동시
    # for source in sources:
    #     print(f"\n🌐 {source['name'].upper()} 뉴스 수집 중...")
    #     articles = fetch_news_from_to(
    #         query="",
    #         start_date=start_date,
    #         end_date=end_date,
    #         source=source["api_name"]
    #     )
    #     save_and_vectorize_langchain(
    #         articles,
    #         source_name=source["name"],
    #         start_date=start_date,
    #         end_date=end_date
    #     )

    # api 호출 없이 파일 벡터화
    for source in sources:
        print(f"\n🌐 {source['name'].upper()} 벡터화 실행 중...")
        load_and_vectorize_from_file(
            source_name=source["name"],
            start_date=start_date,
            end_date=end_date
        )

    client.close()
