import os
from datetime import datetime
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain, LLMChain
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

# article_prompt = PromptTemplate(
#     input_variables=["context", "question"],
#     template="""
# You are a friendly and talkative English tutor. Your main goal is to help the user easily understand English news articles.

# Article:
# {context}

# User asked:
# {question}

# Please follow these instructions carefully:

# [ Article Summary ]

# - Summarize the article using short, clear, and natural paragraphs.
# - Make each paragraph easy to read and friendly for English learners.
# - Add blank lines between paragraphs.

# [ Important Words ]

# - Choose 3~4 important or difficult words.
# - For each word:
#     - Write the word.
#     - Add a simple explanation.
# - Use "-" and indentation to make it easy to read.

# [ Follow-up Question ]

# - Ask one friendly and simple question related to the article.
# - Make sure the entire response looks clean and easy to read.
# """
# )

# tutor_prompt = PromptTemplate(
#     input_variables=["question"],
#     template="""
# You are a friendly and talkative English tutor.

# User asked:

# {question}

# Please answer naturally and help them with vocabulary, grammar, and natural expressions like a human tutor.
# """
# )

korean_tutor_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a friendly English tutor who teaches Korean students.

When you answer, follow these steps:

1. First, give your answer in natural and simple English.
2. Then, explain the meaning in Korean so that Korean students can easily understand.
3. Use simple and friendly Korean expressions when explaining.
4. If necessary, give example sentences both in English and Korean.

User asked:

{question}

Now, please answer.
"""
)

korean_article_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a friendly English tutor who teaches Korean students using news articles.

Article:
{context}

User asked:
{question}

Please follow these steps:

[ Article Summary (EN) ]

- Summarize the article in clear and simple English.
- Use short and friendly sentences.

[ Explanation (KR) ]

- Explain the article and its key points in Korean so that Korean students can understand easily.

[ Important Words (EN -> KR) ]

- Select 3-4 important/difficult words.
- For each word:
    - Write the word (EN)
    - Explain in simple Korean.

[ Follow-up Question (EN) ]

- Ask one friendly and simple English question related to the article.
"""
)



# -------------------------------
# Vector Store (Weaviate)
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
# Helper functions
# -------------------------------

def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

def log_interaction(question, answer, sources):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Q: {question} | A: {answer} | Sources: {sources}\n")

def user_wants_article(user_input: str) -> bool:
    check_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, openai_api_key=OPENAI_API_KEY)

    prompt = f"""
User said: "{user_input}"

Does the user want to read articles or ask for news? Answer only "Yes" or "No".
"""

    result = check_llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return "Yes" in result


# -------------------------------
# Unified Chat Logic
# -------------------------------

# def get_answer(user_input: str):
#     if user_wants_article(user_input):
#         # Article mode
#         docs = vectorstore.similarity_search(user_input, k=2)
#         context = "\n\n".join([doc.page_content for doc in docs])

#         response = llm.invoke(article_prompt.format(context=context, question=user_input)).content
#         source_url = docs[0].metadata.get("url", "") if docs else ""

#     else:
#         # General tutor mode
#         response = llm.invoke(tutor_prompt.format(question=user_input)).content
#         source_url = ""

#     return clean_text(response), source_url

def get_answer(user_input: str):
    if user_wants_article(user_input):
        # Article mode
        docs = vectorstore.similarity_search(user_input, k=2)
        context = "\n\n".join([doc.page_content for doc in docs])

        response = llm.invoke(korean_article_prompt.format(context=context, question=user_input)).content
        source_url = docs[0].metadata.get("url", "") if docs else ""

    else:
        # General tutor mode
        response = llm.invoke(korean_tutor_prompt.format(question=user_input)).content
        source_url = ""

    return clean_text(response), source_url


# -------------------------------
# Main Chatbot Function
# -------------------------------

@traceable(name="run_chatbot")
def run_chatbot(raw_input: str) -> dict:
    question = clean_text(raw_input)

    # Save user input
    memory.save_context({"input": question}, {"answer": ""})

    answer, source_url = get_answer(question)

    # Save generated answer
    memory.save_context({"input": question}, {"answer": answer})

    log_interaction(question, answer, [source_url or "출처 없음"])

    return {
        "answer": answer,
        "source": source_url
    }


