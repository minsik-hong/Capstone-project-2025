import os
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

load_dotenv()

# LLM 설정 (OpenAI API Key 필요)
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # 또는 "gpt-4"
    temperature=0,
)

# Weaviate 연결
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

# VectorStore 불러오기 (뉴스 소스명에 따라 바꿔주세요)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = WeaviateVectorStore(
    client=client,
    embedding=embedding_model,
    index_name="news_bbc",  # 또는 news_cnn
    text_key="text"
)

# 대화 메모리 & QA 체인 생성
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer" 
)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

# 대화 루프 시작
def chat():
    print("🗞️ 뉴스 기반 RAG 챗봇에 오신 걸 환영합니다!")
    print("종료하려면 'exit'을 입력하세요.\n")
    while True:
        question = input("👤 질문: ")
        if question.lower() in ("exit", "quit"):
            print("👋 종료합니다.")
            break
        response = qa_chain.invoke({"question": question})
        answer = response["answer"]
        sources = [
            doc.metadata.get("url", "출처 없음")
            for doc in response.get("source_documents", [])
        ]
        print(f"\n🤖 답변: {answer}")
        print("🔗 출처:")
        for src in sources:
            print(f" - {src}")
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    chat()
    client.close()