from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 모델 선택 (Hugging Face or OpenAI)
USE_OPENAI = True
openai.api_key = os.getenv("OPENAI_API_KEY")
hf_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """ 입력된 텍스트를 벡터로 변환 """
    if USE_OPENAI:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]
    else:
        return hf_model.encode(text)