# backend/services/chatbot_test.py
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import HumanMessage
from langchain.chains import LLMChain
from langchain_core.runnables import RunnableSequence


from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

from services.memory_manager import UserSessionMemoryManager
from services.prompt_templates import PROMPTS
from services.profile_injector import inject_profile_into_prompt
from db.models.user import UserProfile
from sqlalchemy.orm import Session

from langchain_core.runnables import RunnableSequence

# ========== 환경 변수 설정 ==========
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "news-chatbot")
os.environ["LANGCHAIN_TRACING_V2"] = "true" 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "News_bbc")

# ========== LLM 및 Vectorstore 초기화 ==========
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3, openai_api_key=OPENAI_API_KEY)

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

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = WeaviateVectorStore(
    client=client,
    embedding=embedding_model,
    index_name=WEAVIATE_INDEX_NAME,
    text_key="content"
)

# ========== 유틸 함수 ==========
def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

def log_interaction(question, answer, source_url):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Q: {question} | A: {answer} | Source: {source_url}\n")

def should_use_news(question: str) -> bool:
    judge_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, openai_api_key=OPENAI_API_KEY)
    prompt = f"""
User input: "{question}"

Is this about news, facts, or current issues? (Answer only yes or no)
"""
    result = judge_llm.invoke([HumanMessage(content=prompt)]).content.strip().lower()
    return result == "yes"

# ========== 메인 함수 ==========
MODE_MAPPING = {
    "summary": "summary",
    "vocab": "vocab_quiz",
    "grammar": "grammar_quiz",
    "dialogue": "dialogue",
    "": "default"
}

def run_chatbot_personalized(user_id: str, session_id: str, user_input: str, mode: str, db: Session):
    mode = MODE_MAPPING.get(mode, "default")
    question = clean_text(user_input)

    # 메모리 매니저 초기화
    memory_manager = UserSessionMemoryManager(db, session_id, user_id)
    memory = memory_manager.get_memory()

    # 첫 인사 처리
    if not memory.chat_memory.messages:
        welcome = "안녕하세요! 저는 최신 뉴스로 영어를 자연스럽게 가르쳐주는 AI 튜터입니다. 모드를 선택해서 영어를 효과적으로 배울 수 있어요!"
        memory_manager.save_message("bot", welcome)
        return {"answer": welcome, "source": ""}

    # 뉴스 기반 모드 확인
    use_news = mode in ["summary", "vocab_quiz", "grammar_quiz", "dialogue"]
    
    # default 모드에서는 뉴스 사용 여부를 판단
    # if mode == "default":
    #     use_news = should_use_news(question)

    # default 모드에서는 news 사용 안 함
    news_text, source_url = "", ""
    if use_news:
        docs = vectorstore.similarity_search(question, k=1)
        if docs:
            news_text = docs[0].page_content
            source_url = docs[0].metadata.get("url", "")

    # 프롬프트 준비
    prompt = PROMPTS.get(mode, PROMPTS["default"])
    # 사용자 프로필 불러오기
    profile_obj = UserProfile.get(db, user_id)
    if profile_obj:
        profile_dict = {
            "level": profile_obj.profile_level,
            "interests": profile_obj.interests,
            "weaknesses": profile_obj.weaknesses,
            "summary": profile_obj.summary,
        }
        # 기존 PROMPTS.get(...) 결과와 결합
        base_prompt = PROMPTS.get(mode, PROMPTS["default"])
        prompt = inject_profile_into_prompt(profile_dict, base_prompt)
    else:
        prompt = PROMPTS.get(mode, PROMPTS["default"])
    
    inputs = {}
    if "input" in prompt.input_variables:
        inputs["input"] = question
    if "news" in prompt.input_variables:
        inputs["news"] = news_text

    # 모든 모드에서 memory 사용 (follow-up 대응 가능)
    chain = LLMChain(
        llm=llm, 
        prompt=prompt, 
        memory=memory,
        verbose=True,
        )
    result = chain.invoke(inputs)
    response = clean_text(result["text"])

    # 대화 저장
    memory_manager.save_message("user", question)
    memory_manager.save_message("bot", response)

    log_interaction(question, response, source_url)

    return {"answer": response, "source": source_url}
