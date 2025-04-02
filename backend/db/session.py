
from sqlalchemy import create_engine # 데이터베이스 엔진 생성을 위한 모듈
from sqlalchemy.orm import sessionmaker # 세션 및 베이스 클래스 생성 모듈
from backend.db.base import Base

DATABASE_URL = "sqlite:///./users.db"

# SQLite 엔진 생성 (멀티 스레드 허용 설정)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 세션을 가져오는 함수
def get_db():
    db = SessionLocal() # 세션 인스턴스 생성
    try:
        yield db # 세션을 호출자에게 반환
    finally:
        db.close() # 작업 완료 후 세션 닫기

        
