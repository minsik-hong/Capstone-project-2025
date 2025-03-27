# test_query.py
from news_ingest import VectorDB, get_embedding

query = input("검색할 키워드를 입력하세요: ")
vector = get_embedding(query)

vdb = VectorDB()
results = vdb.search(vector, top_k=5)

print("\n🔎 검색 결과:")
for i, item in enumerate(results["metadatas"]):
    print(f"{i+1}. {item['title']}")
    print(f"   URL: {item['url']}")
