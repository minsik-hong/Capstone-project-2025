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

# Load .env
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(dotenv_path=os.path.join(ROOT_DIR, ".env"))

# Environment settings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "news-chatbot"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "News_bbc")

# LLM setup
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY
)

# Tutor Prompt (for general English tutor chat)
tutor_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a friendly and talkative English tutor.

User asked:

{question}

Please answer naturally and help them with vocabulary, grammar, and natural expressions like a human tutor.

"""
)

tutor_chain = LLMChain(llm=llm, prompt=tutor_prompt)

# Article prompt
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a friendly and talkative English tutor. Your main goal is to help the user easily understand English news articles.

Article:
{context}

User asked:
{question}

Please follow these instructions carefully:

[ Article Summary ]

- Summarize the article using short and simple sentences.
- Use "•" for each point.
- Add blank lines between ideas.

[ Important Words ]

- Choose 3~4 important or difficult words.
- For each word:
    - Write the word.
    - Add a simple explanation.
- Use "-" and indentation to make it easy to read.

[ Follow-up Question ]

- Ask one friendly and simple question related to the article.
- Make sure the entire response looks clean and easy to read.

Your final response should be:
- Plain text only
- Structured with sections and symbols
- Very easy for English learners to read

"""
)


# Weaviate connection
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

# Embedding & Vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = WeaviateVectorStore(
    client=client,
    embedding=embedding_model,
    index_name=WEAVIATE_INDEX_NAME,
    text_key="content"
)

# Conversation memory
memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    output_key="answer",
    return_messages=True
)

# Article QA chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    memory=memory,
    combine_docs_chain_kwargs={"prompt": custom_prompt},
    return_source_documents=True,
    output_key="answer"
)

# Helper functions
def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

def log_interaction(question, answer, sources):
    with open("chat_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Q: {question} | A: {answer} | Sources: {sources}\n")

# User intent detection (whether they want article or just tutor)
def user_wants_article(user_input: str) -> bool:
    chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, openai_api_key=OPENAI_API_KEY)

    prompt = f"""
User said: "{user_input}"

Does the user want to read articles or ask for news? Answer only 'Yes' or 'No'.
"""

    result = chat.invoke([HumanMessage(content=prompt)]).content.strip()
    return "Yes" in result

# -------------------------------
# External chatbot function
# -------------------------------

@traceable(name="run_chatbot")
def run_chatbot(raw_input: str) -> dict:
    question = clean_text(raw_input)

    if user_wants_article(question):
        # Article mode
        response = qa_chain.invoke({"question": question})
        source_url = ""
        if response.get("source_documents"):
            first_doc = response["source_documents"][0]
            url = first_doc.metadata.get("url")
            if url:
                source_url = url  # valid url only

        final_answer = clean_text(response.get("answer", "답변 생성 실패"))

    else:
        # Normal Tutor mode
        final_answer = tutor_chain.run(question=question)
        source_url = ""  # no source

    log_interaction(question, final_answer, [source_url or "출처 없음"])

    return {
        "answer": final_answer,
        "source": source_url  # always string ("" or url)
    }

