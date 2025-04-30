import os
import re
from datetime import datetime
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

from langchain.chains.summarize import load_summarize_chain
from langsmith import traceable

# .env 로드
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

# 환경 변수
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "news-chatbot"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "News_bbc")

# system_prompt = (
#     "You are a friendly and knowledgeable English tutor who also provides news information. "
#     "You explain English vocabulary, grammar, and expressions using current news articles. "
#     "You ask follow-up questions to help the user practice English conversation."
# )

# LLM 설정
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY,
    # model_kwargs={"system_prompt": system_prompt}
)

# Weaviate 연결
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

# Embedding & Vectorstore 설정
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = WeaviateVectorStore(
    client=client,
    embedding=embedding_model,
    index_name=WEAVIATE_INDEX_NAME,
    text_key="content"
)

# 요약 기반 메모리
memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    output_key="answer",
    return_messages=True
)

# QA 체인 구성
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

# 전역 변수
last_question = {"question": ""}

# -------------------------------
# 주요 함수들
# -------------------------------

def detect_followup_type(q: str) -> str:
    followup_phrases = {
        "more": [r"\b(more please|more|tell me more|추가로|더 알려줘|관련 more|좀 더 자세히)\b"],
        "similar": [r"\b(similar|another one|다른 주제|비슷한 주제|다른 걸로|유사한 뉴스)\b"]
    }
    for followup_type, patterns in followup_phrases.items():
        for pattern in patterns:
            if re.search(pattern, q, re.IGNORECASE):
                return followup_type
    return "original"

def preprocess_question(q: str) -> str:
    q = q.lower().strip()
    followup_type = detect_followup_type(q)
    if followup_type == "more":
        return f"이전 질문에 대해 더 자세히 알려줘: {last_question['question']}"
    elif followup_type == "similar":
        return f"비슷하지만 다른 주제의 기사를 보여줘: {last_question['question']}"
    else:
        last_question["question"] = q
        return q

def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

def summarize_doc(doc) -> str:
    summary_chain = load_summarize_chain(llm=llm, chain_type="refine")
    try:
        result = summary_chain.invoke([doc])
        if isinstance(result, dict):
            return result.get("output_text", "요약 없음")
        return result
    except Exception as e:
        print(f"요약 실패: {e}")
        return "요약 실패"

def log_interaction(question, answer, sources, base_question=None):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Q: {question} | A: {answer} | Sources: {sources}")
        if base_question:
            f.write(f" | BaseQ: {base_question}")
        f.write("\n")

# -------------------------------
# 외부에서 호출할 함수
# -------------------------------

@traceable(name="run_chatbot")
def run_chatbot(raw_input: str) -> dict:
    question = preprocess_question(clean_text(raw_input))
    response = qa_chain.invoke({"question": question})

    top_doc = response.get("source_documents", [])[0] if response.get("source_documents") else None

    if top_doc:
        summary = summarize_doc(top_doc)
        source = top_doc.metadata.get("url", "출처 없음")
    else:
        summary = "관련 문서를 찾을 수 없습니다"
        source = "출처 없음"

    final_answer = clean_text(summary)

    followup_type = detect_followup_type(raw_input)
    base_q = last_question["question"] if followup_type in ["more", "similar"] else None

    log_interaction(raw_input, final_answer, [source], base_question=base_q)

    return {
        "answer": final_answer,
        "source": source
    }