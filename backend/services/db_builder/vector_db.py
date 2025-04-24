import chromadb
from chromadb.config import Settings

class VectorDB:
    def __init__(self, collection_name="news_vectors"):
        self.client = chromadb.Client(Settings(persist_directory="data/vector_db"))
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_vector(self, vector, metadata):
        # 중복 방지: 동일한 URL이 이미 존재하는지 확인
        existing = self.collection.query(
            where={"url": metadata["url"]}, n_results=1
        )
        if existing["ids"]:
            print(f"⚠️ 이미 존재하는 URL: {metadata['url']}")
            return
        self.collection.add(embeddings=[vector], metadatas=[metadata])

    def search(self, query_vector, top_k=5):
        results = self.collection.query(query_embeddings=[query_vector], n_results=top_k)
        return results

    def get_metadata(self, index):
        document = self.collection.get(ids=[index])
        return {
            "title": document["metadatas"][0]["title"],
            "summary": document["documents"][0],
            "url": document["metadatas"][0]["url"]
        }