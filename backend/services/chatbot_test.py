import os
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

# ✅ 루트 디렉토리의 .env 로드
# chatbot_test.py → backend/services/chatbot_test.py 기준
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

# ✅ 환경변수에서 정보 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "news_bbc")

# ✅ LLM 설정
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# ✅ Weaviate 연결
connection_params = ConnectionParams.from_params(
    http_host=WEAVIATE_HOST,
    http_port=WEAVIATE_PORT,
    http_secure=False,
    grpc_host=WEAVIATE_HOST,
    grpc_port=WEAVIATE_GRPC_PORT,
    grpc_secure=False
)
client = WeaviateClient(connection_params=connection_params)
client.connect()

# ✅ 벡터스토어 및 QA 체인 초기화
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = WeaviateVectorStore(
    client=client,
    embedding=embedding_model,
    index_name=WEAVIATE_INDEX_NAME,
    text_key="text"
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

def clean_text(text: str) -> str:
    """UTF-8 인코딩 불가능한 문자를 제거하는 유틸 함수"""
    return text.encode("utf-8", "ignore").decode("utf-8")

def run_qa(question: str):
    """질문을 받아서 RAG 기반 응답을 반환하는 함수 (입력 정리 포함)"""
    question = clean_text(question)
    response = qa_chain.invoke({"question": question})
    
    sources = []
    for doc in response.get("source_documents", []):
        url = doc.metadata.get("url", "출처 없음")
        sources.append(clean_text(url))

    return {
        "answer": clean_text(response["answer"]),
        "sources": sources
    }


def close_client():
    client.close()

# CLI 모드
def chat():
    print("🗞️ 뉴스 기반 RAG 챗봇에 오신 걸 환영합니다!")
    print("종료하려면 'exit'을 입력하세요.\n")
    while True:
        question = input("👤 질문: ")
        if question.lower() in ("exit", "quit"):
            print("👋 종료합니다.")
            break
        result = run_qa(question)
        print(f"\n🤖 답변: {result['answer']}")
        print("🔗 출처:")
        for src in result['sources']:
            print(f" - {src}")
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    try:
        chat()
    finally:
        close_client()
