
from sqlalchemy import create_engine # 데이터베이스 엔진 생성을 위한 모듈
from sqlalchemy.orm import sessionmaker # 세션 및 베이스 클래스 생성 모듈
from db.base import Base
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경변수 로드

# PostgreSQL용 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다.")

# PostgreSQL 엔진 생성 (connect_args 제거)
engine = create_engine(DATABASE_URL)

# 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 세션을 가져오는 함수
def get_db():
    db = SessionLocal() # 세션 인스턴스 생성
    try:
        yield db # 세션을 호출자에게 반환
    finally:
        db.close() # 작업 완료 후 세션 닫기

# DB 초기화 함수 추가
def init_db():
    Base.metadata.create_all(bind=engine)       
