import os
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

# ✅ 환경 변수 로드
load_dotenv(dotenv_path="/Users/hongminsik/Desktop/Capstone-project-2025/backend/.env")
print("✅ API KEY:", os.getenv("OPENAI_API_KEY")[:8], "...")  # 앞 8자리만 출력

# ✅ Weaviate v4 연결 및 연결 시작
connection_params = ConnectionParams.from_params(
    http_host="localhost",
    http_port=8080,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False
)
client = WeaviateClient(connection_params=connection_params)
client.connect()  # 🔥 연결 필요!

# ✅ 벡터 스토어 로드
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = WeaviateVectorStore(
    client=client,
    index_name="news_bbc",
    embedding=embedding_model,
    text_key="text"  # ✅ 실제 Weaviate 저장 필드명으로 수정
)

# ✅ 프롬프트 템플릿 정의 (LLM 가이드 포함)
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert in summarizing and answering questions based on news articles.

Here is the content retrieved from related news articles:
---------------------
{context}
---------------------

Based on the above information, answer the question.  
If the information is not found in the context, politely respond with "There is no relevant information in the articles."

Question: {question}
Answer:
"""
)

# ✅ RAG QA 체인 구성
retriever = vector_store.as_retriever(search_kwargs={"k": 6}) # 6개의 유사 문서 검색
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.5, # 낮을수록 보수적인 답변
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff",
    chain_type_kwargs={"prompt": custom_prompt}
)

# ✅ 테스트 쿼리
query = "please give me news about technology."
result = qa_chain.invoke(query)

print("\n🧠 Answer:")
print(result["result"])

print("\n📄 Source Documents:")
seen_urls = set()
for doc in result["source_documents"]:
    title = doc.metadata.get("title")
    url = doc.metadata.get("url")
    if url not in seen_urls:
        print("-", title, "|", url)
        seen_urls.add(url)


# ✅ Weaviate 연결 종료
client.close()
print("\n🔌 Weaviate 연결 종료")