# backend/services/chatbot_test.py
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import HumanMessage
from langchain.chains import LLMChain
from langsmith import traceable
from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

from services.memory_manager import UserSessionMemoryManager
from db.session import get_db
from sqlalchemy.orm import Session

# ========== 환경 변수 설정 ==========

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

os.environ["TOKENIZERS_PARALLELISM"] = "false"
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
vectorstore = WeaviateVectorStore(client=client, embedding=embedding_model, index_name=WEAVIATE_INDEX_NAME, text_key="content")

# ========== Memory ==========

memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", return_messages=True)

# ========== Prompt ==========

PROMPTS = {
    "default": ChatPromptTemplate.from_template("""
You are a friendly and casual English tutor for Korean students. 
Your job is to help them improve English naturally through conversation.

**Important Rules**
- Do not include or explain harmful, violent, sexual, or inappropriate content.
- Only use safe, neutral, and educational content.

Provide answers in two parts:

**[English]**
(Natural conversation)

**[한국어]**
(Explanation in Korean)

---

**Examples**

User: Hi! How are you?

Tutor:

**[English]**
"I'm doing great! How about you?"

**[한국어]**
"저는 아주 좋아요! 당신은 어때요?"

---

User: Can you tell me about today's news?

News: The city plans to build more parks to improve public health.

Tutor:

**[English]**
"Sure! The city will build more parks so people can stay healthy and enjoy nature."

**[한국어]**
"물론이죠! 도시는 사람들이 더 건강하고 자연을 즐길 수 있도록 더 많은 공원을 지을 예정이에요."

---

User Input:
{input}

Tutor:
"""),

    "summary": ChatPromptTemplate.from_template("""
You are an English tutor helping Korean students. 
Your task is to summarize news articles in very simple and easy English.

**Important Rules**
- Do not include or explain harmful, violent, sexual, or inappropriate content.
- Only use safe, neutral, and educational content.

Provide answers in two parts:

**[English]**
(Summary)

**[한국어]**
(Summary in Korean)

---

News:
{news}

Summary:
"""),

    "vocab_quiz": ChatPromptTemplate.from_template("""
You are an English tutor helping Korean students.
Your job is to make vocabulary quizzes from news articles using the words from the article.

**Important Rules**
- Do not include or explain harmful, violent, sexual, or inappropriate content.
- Only use safe, neutral, and educational content.

Create 3 vocabulary questions:
- Focus on words from the news article.
- Mix question types: meaning guess (context), synonym, antonym, and fill-in-the-blank.
- Provide 4 options (A, B, C, D).
- At the end, provide correct answers and simple explanations.

Provide answers in two parts:

**[English]**
(Quiz + Answers + Explanation)

**[한국어]**
(Quiz + Answers + Explanation in Korean)

---

**Examples**

User: Give me a vocabulary quiz from this news.

News: The global economy is recovering slowly after the pandemic, but inflation remains high.

Tutor:

**[English]**

1. What does "recovering" most likely mean in this news?  
A) becoming worse  
B) getting better  
C) staying the same  
D) going back

2. What is a synonym of "inflation"?  
A) price rise  
B) vacation  
C) pollution  
D) education

3. He will ______ from the illness soon.  
A) become  
B) recover  
C) increase  
D) avoid

**Answers:**  
1 B (getting better)  
2 A (price rise)  
3 B (recover)

**[한국어]**

1. recover는 여기서 "나아지고 있다"라는 뜻이에요.  
2. inflation의 유의어는 "가격 상승"입니다.  
3. 그는 곧 병에서 회복할 것입니다.

**정답:**  
1번 B  
2번 A  
3번 B

---

News:
{news}

Vocabulary Quiz:
"""),

"grammar_quiz": ChatPromptTemplate.from_template("""
You are an English tutor helping Korean students.
Your job is to make grammar and sentence pattern quizzes from news articles.

**Important Rules**
- Do not include or explain harmful, violent, sexual, or inappropriate content.
- Only use safe, neutral, and educational content.

Create 3 multiple-choice grammar questions:
- Focus on sentence patterns, tense, articles, prepositions, modals, etc.
- Provide 3 or 4 options (A, B, C, D).
- At the end, provide correct answers with simple and clear explanations for each.

Provide answers in two parts:

**[English]**
(Quiz + Answers + Explanation)

**[한국어]**
(Quiz + Answers + Explanation in Korean)

---

**Examples**

User: Give me a grammar quiz from this news.

News: Scientists are expected to announce the results next month.

Tutor:

**[English]**

1. What is the correct pattern for future expectation?  
A) are expecting to  
B) are expected to  
C) were expected to  
D) are expect

2. Choose the correct sentence.  
A) Scientists expected to announce results next month.  
B) Scientists are expected to announce the results next month.  
C) Scientists are expecting the results next month.


3. What does "are expected to" mean?  
A) Something will likely happen  
B) Something already happened  
C) Something impossible

→ **Answer:**
1. B
- **Explanation:** "Are expected to" is the correct passive form used to express a general future expectation.
2. B
- **Explanation:** "Are expected to" shows that others believe scientists will announce the results next month.
3. A
- **Explanation:** "Are expected to" means something will likely happen in the future.

**[한국어]**

1. 미래 예측을 나타내는 올바른 표현은 무엇입니까?  
→ **정답: B (are expected to)**  
**해설:** 일반적인 미래 예상 표현으로 수동형이 쓰였습니다.

2. 올바른 문장을 고르세요.  
→ **정답: B**  
**해설:** 과학자들이 결과를 발표할 것으로 예상된다는 뜻입니다.

3. "are expected to"의 의미는 무엇입니까?  
→ **정답: A (가능성이 높다)**  
**해설:** 미래에 일어날 가능성이 높은 일을 나타냅니다.

---

News:
{news}

Grammar Quiz:
"""),
"dialogue": ChatPromptTemplate.from_template("""
You are an English tutor helping Korean students.
Your task is to create a short and natural dialogue based on news articles.

**Important Rules**
- Do not include or explain harmful, violent, sexual, or inappropriate content.
- Only use safe, neutral, and educational content.
- Make the dialogue practical and natural as if two people are talking in real life.
- Use simple and clear sentences suitable for learning.
- Add small expressions for natural flow (e.g. "Oh really?", "That's nice", "I see", etc.)

Provide answers in two parts:

**[English]**
(Dialogue)

**[한국어]**
(Dialogue in Korean)

---

**Examples**

User: Make a dialogue based on this news.

News: A new law will ban plastic bags in supermarkets starting next year.

Tutor:

**[English]**

A: Did you hear about the new law?  
B: No, what is it?  
A: Supermarkets will stop giving plastic bags from next year.  
B: Oh really? That’s good for the environment.  
A: Yeah, we should bring our own bags when we shop.

**[한국어]**

A: 새 법안 들었어?  
B: 아니, 뭐야?  
A: 내년부터 슈퍼마켓에서 비닐봉지를 주지 않을 거래.  
B: 아 정말? 그거 환경에 좋겠다.  
A: 응, 이제 장볼 때 에코백 가져가야겠네.

---

News:
{news}

Dialogue:
"""),

    "answer_reveal": ChatPromptTemplate.from_template("""
You are an English tutor who is now revealing the correct answers for the quiz given earlier.

**Important Rules**
- Do not include or explain harmful, violent, sexual, or inappropriate content.
- Only use safe, neutral, and educational content.

Provide answers in two parts:

**[English]**
(Answers)

**[한국어]**
(Answers in Korean)

---

Quiz:
{quiz_content}

Answers:
""")
}

# ========== Helper Functions ==========

def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

def log_interaction(question, answer, source_url):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Q: {question} | A: {answer} | Source: {source_url}\n")

def save_and_return_answer(user_input: str, answer: str, source_url: str = "") -> dict:
    memory.save_context({"input": user_input}, {"answer": answer})
    return {"answer": answer, "source": source_url}

def should_use_news(question: str) -> bool:
    judge_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, openai_api_key=OPENAI_API_KEY)
    prompt = f"""
User input: "{question}"

Is this about news, facts, or current issues? (Answer only yes or no)
"""
    result = judge_llm.invoke([HumanMessage(content=prompt)]).content.strip().lower()
    return result == "yes"

def summarize_news(docs):
    if not docs:
        return "", ""

    news_text = "\n\n".join([doc.page_content for doc in docs])
    summary_prompt = ChatPromptTemplate.from_template("""
Summarize the following news articles in simple English.

Articles:
{articles}
""")
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
    result = summary_chain.invoke({"articles": news_text})
    source_url = docs[0].metadata.get("url", "") if docs else ""
    return result["text"], source_url

# ========== 메인 챗봇 함수 ==========

MODE_MAPPING = {
    "summary": "summary",
    "vocab": "vocab_quiz",
    "grammar": "grammar_quiz",
    "dialogue": "dialogue",
    "": "default"  # 빈값일 때
}


def run_chatbot_personalized(user_id: str, session_id: str, user_input: str, mode: str, db: Session):
    mode = MODE_MAPPING.get(mode, "default")
    question = clean_text(user_input)

    # 사용자 맞춤 memory
    memory_manager = UserSessionMemoryManager(db, session_id, user_id)
    memory = memory_manager.get_memory()

    # 첫 인사
    if not memory.chat_memory.messages:
        welcome = "안녕하세요! 저는 최신 뉴스로 영어를 자연스럽게 가르쳐주는 AI 튜터입니다. 모드를 선택해서 영어를 효과적으로 배울 수 있어요!"
        memory_manager.save_message("bot", welcome)
        return {"answer": welcome, "source": ""}

    # 뉴스 사용 여부 결정
    use_news = mode in ["summary", "vocab_quiz", "grammar_quiz", "dialogue"]
    if mode == "default":
        use_news = should_use_news(question)

    news_summary, source_url = "", ""
    if use_news:
        docs = vectorstore.similarity_search(question, k=5)
        news_summary, source_url = summarize_news(docs)

    # 프롬프트 & 입력 구성
    prompt = PROMPTS.get(mode, PROMPTS["default"])
    inputs = {}
    if "input" in prompt.input_variables:
        inputs["input"] = question
    if "news" in prompt.input_variables:
        inputs["news"] = news_summary

    chain = LLMChain(llm=llm, prompt=prompt, memory=memory if mode == "default" else None)
    result = chain.invoke(inputs)
    response = clean_text(result["text"])

    if mode == "default":
        memory_manager.save_message("user", question)
        memory_manager.save_message("bot", response)

    log_interaction(question, response, source_url)

    return {"answer": response, "source": source_url}


@traceable(name="run_chatbot")
def run_chatbot(user_input: str, mode: str = "") -> dict:
    # 프론트에서 온 mode 값을 backend용으로 변환
    mode = MODE_MAPPING.get(mode, "default")

    question = clean_text(user_input)

    # 최초 대화
    if not memory.chat_memory.messages:
        welcome = "안녕하세요! 저는 최신 뉴스로 영어를 자연스럽게 가르쳐주는 AI 튜터입니다. 모드를 선택해서 영어를 효과적으로 배울 수 있어요!"
        memory.save_context({"input": ""}, {"answer": welcome})
        return {"answer": welcome, "source": ""}

    # 뉴스 사용 여부 결정
    if mode == "default":
        # default 모드일 때만 뉴스 사용 여부 판단
        use_news = should_use_news(question)
    else:
        # 모드가 지정된 경우 summary, vocab_quiz, grammar_quiz, dialogue만 뉴스 사용
        use_news = mode in ["summary", "vocab_quiz", "grammar_quiz", "dialogue"]

    news_summary = ""
    source_url = ""

    if use_news:
        docs = vectorstore.similarity_search(question, k=5)
        news_summary, source_url = summarize_news(docs)

    # 프롬프트 선택
    prompt = PROMPTS.get(mode, PROMPTS["default"])

    # 입력 구성
    inputs = {}
    if "input" in prompt.input_variables:
        inputs["input"] = question
    if "news" in prompt.input_variables:
        inputs["news"] = news_summary

    chain = LLMChain(llm=llm, prompt=prompt, memory=memory if mode == "default" else None, verbose=True)
    result = chain.invoke(inputs)
    response = clean_text(result["text"])

    if not use_news:
        source_url = ""

    if mode == "default":
        memory.save_context({"input": question}, {"answer": response})

    log_interaction(question, response, source_url)

    return {"answer": response, "source": source_url}


# ========== 테스트 모드 ==========

if __name__ == "__main__":
    print("💬 Chatbot Test Mode Started!")

    if not memory.chat_memory.messages:
        welcome = "안녕하세요! 최신 뉴스로 영어를 가르쳐주는 AI 튜터입니다."
        print("\nAI:", welcome)
        memory.save_context({"input": ""}, {"answer": welcome})

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "종료"]:
            print("👋 Bye!")
            break

        result = run_chatbot(user_input)
        print("\nAI:", result["answer"])

        if result["source"]:
            print("[참고한 뉴스 출처]:", result["source"])
