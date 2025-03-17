# 환경 설정

import os  # 운영 체제와 상호작용하기 위한 모듈
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하기 위한 모듈

load_dotenv()  # .env 파일에서 환경 변수 로드

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # NewsAPI의 API 키를 환경 변수에서 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API 키를 환경 변수에서 가져오기
VECTOR_DB_PATH = "data/vector_db"  # 벡터 DB 파일 경로 설정