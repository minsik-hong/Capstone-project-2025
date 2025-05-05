import os
from datetime import datetime
from dotenv import load_dotenv

from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langsmith import traceable
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams
from langchain.schema import HumanMessage

# -------------------------------
# Environment & Settings
# -------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "news-chatbot"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "News_bbc")


# -------------------------------
# LLM
# -------------------------------

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY
)


# -------------------------------
# Prompts
# -------------------------------

# korean_tutor_prompt = PromptTemplate(
#     input_variables=["question"],
#     template="""
# You are a friendly English tutor who teaches Korean students.

# When you answer, follow these steps:

# 1. Answer naturally and simply in English.
# 2. Explain the meaning in Korean.
# 3. Use friendly Korean expressions.

# User asked:

# {question}

# Now, please answer.
# """
# )

korean_article_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a friendly English tutor who teaches Korean students using news articles.

Article:
{context}

User asked:
{question}

[ Article Summary (EN) ]
- Summarize in clear and simple English.

[ Explanation (KR) ]
- Explain in Korean.

[ Important Words (EN -> KR) ]
- Pick 3~4 words, explain them in Korean.

[ Follow-up Question (EN) ]
- Ask one question in English.
"""
)

vocab_quiz_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an English quiz maker for Korean students.

Article:
{context}

User asked:
{question}

Make a vocabulary quiz from the article:
- Select 3 difficult words.
- For each, make a multiple-choice question.
- Provide answers and explain each in Korean.
"""
)

grammar_quiz_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an English grammar quiz maker for Korean students.

Article:
{context}

User asked:
{question}

Make a grammar quiz from the article:
- Select 3 grammar points.
- For each, make a question (multiple choice or fill in the blank).
- Explain answers in Korean.
"""
)

content_quiz_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an English reading comprehension quiz maker for Korean students.

Article:
{context}

User asked:
{question}

Make a content quiz:
- Make 3 questions about the content.
- Multiple choice preferred.
- Explain the answers in Korean.
"""
)

# free_chat_prompt = PromptTemplate(
#     input_variables=["question"],
#     template="""
# You are a friendly English teacher who enjoys casual conversation.

# User asked:

# {question}

# Please respond in natural and friendly English like a real person having a chat. If the user asks for explanation, explain simply in Korean as well.
# """
# )

default_tutor_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a kind and natural English tutor for Korean students.

When the user asks a question, do these:

1. Respond naturally in English, like casual conversation.
2. If the sentence is difficult, provide simple Korean explanation too.
3. Use friendly expressions as if you are speaking with a student.

User asked:

{question}

Please answer.
"""
)


# -------------------------------
# Vector Store
# -------------------------------

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


# -------------------------------
# Unified Memory
# -------------------------------

memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    output_key="answer",
    return_messages=True
)


# -------------------------------
# Helper Functions
# -------------------------------

def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

def log_interaction(question, answer, sources):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Q: {question} | A: {answer} | Sources: {sources}\n")

def detect_intent(user_input: str) -> str:
    check_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, openai_api_key=OPENAI_API_KEY)

    prompt = f"""
User said: "{user_input}"

Classify the intent as only one of:
- free_chat (casual chat or basic English QnA)
- tutor (English learning, explain in Korean)
- article
- vocab_quiz
- grammar_quiz
- content_quiz
"""

    result = check_llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return result


# -------------------------------
# Unified Chat Logic
# -------------------------------

def get_answer(user_input: str, intent: str):
    # 전문 모드일 경우만 기사 기반 벡터 검색
    if intent in ["article", "vocab_quiz", "grammar_quiz"]:
        docs = vectorstore.similarity_search(user_input, k=2)
        context = "\n\n".join([doc.page_content for doc in docs])
        source_url = docs[0].metadata.get("url", "") if docs else ""
    else:
        context = ""
        source_url = ""

    # intent 에 따른 응답 처리
    if intent == "article":
        response = llm.invoke(korean_article_prompt.format(context=context, question=user_input)).content
    elif intent == "vocab_quiz":
        response = llm.invoke(vocab_quiz_prompt.format(context=context, question=user_input)).content
    elif intent == "grammar_quiz":
        response = llm.invoke(grammar_quiz_prompt.format(context=context, question=user_input)).content
    else:
        # 기본 → 자연스럽고 친절한 튜터 + 프리챗
        response = llm.invoke(default_tutor_prompt.format(question=user_input)).content

    return clean_text(response), source_url


# -------------------------------
# Main Chatbot Function
# -------------------------------

@traceable(name="run_chatbot")
def run_chatbot(raw_input: str, mode: str = "") -> dict:
    question = clean_text(raw_input)
    memory.save_context({"input": question}, {"answer": ""})

    # 전문 모드가 아니면 intent → default 모드 (free chat + tutor)
    intent = mode if mode in ["article", "vocab_quiz", "grammar_quiz"] else "default"

    answer, source_url = get_answer(question, intent)

    memory.save_context({"input": question}, {"answer": answer})
    log_interaction(question, answer, [source_url or "출처 없음"])

    return {
        "answer": answer,
        "source": source_url
    }
