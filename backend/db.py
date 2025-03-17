# 데이터베이스 설정 - SQLite 임시사용

from sqlalchemy import create_engine  # 데이터베이스 엔진 생성을 위한 모듈
from sqlalchemy.orm import sessionmaker, declarative_base  # 세션 및 베이스 클래스 생성 모듈

DATABASE_URL = "sqlite:///./news_learning.db"  # SQLite 데이터베이스 파일 경로 설정

# 데이터베이스 엔진 생성 (SQLite 사용, 동일 스레드에서만 연결 허용 비활성화)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 로컬 생성 (자동 커밋 및 자동 플러시 비활성화)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 클래스 생성을 위한 베이스 클래스
Base = declarative_base()

# 데이터베이스 세션을 가져오는 함수
def get_db():
    db = SessionLocal()  # 세션 인스턴스 생성
    try:
        yield db  # 세션을 호출자에게 반환
    finally:
        db.close()  # 작업 완료 후 세션 닫기