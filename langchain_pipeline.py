from langchain.chains import SequentialChain
from langchain.steps import Step
from .backend.chatbot.db_builder.news_fetcher import fetch_news
from .backend.chatbot.db_builder.embedding import get_embedding
from .backend.chatbot.db_builder.vector_db import VectorDB

class FetchNewsStep(Step):
    def run(self, query, source):
        return fetch_news(query, source)

class EmbedNewsStep(Step):
    def run(self, articles):
        for article in articles:
            if article["content"]:
                article["embedding"] = get_embedding(article["content"])
        return articles

class StoreInVectorDBStep(Step):
    def __init__(self):
        self.vector_db = VectorDB()

    def run(self, articles):
        for article in articles:
            if "embedding" in article:
                metadata = {
                    "title": article["title"],
                    "url": article["url"]
                }
                self.vector_db.add_vector(article["embedding"], metadata)
        return "뉴스 데이터를 벡터 DB에 저장했습니다."

def main():
    chain = SequentialChain(steps=[
        FetchNewsStep(),
        EmbedNewsStep(),
        StoreInVectorDBStep()
    ])

    result = chain.run(query="technology", source="bbc-news")
    print(result)

if __name__ == "__main__":
    main()