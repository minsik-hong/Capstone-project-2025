# 회원 정보 데이터베이스 설정 - SQLite 사용
import sqlite3 # SQLite3 사용을 위한 모듈
from sqlalchemy import create_engine  # 데이터베이스 엔진 생성을 위한 모듈
from sqlalchemy.orm import sessionmaker  # 세션 생성 모듈
from sqlalchemy.ext.declarative import declarative_base  # 베이스 클래스 생성을 위한 모듈

# SQLite 데이터베이스 파일 경로
SQLALCHEMY_DATABASE_URL = "sqlite:///./user_info.db"

# 데이터베이스 엔진 생성 (SQLite 사용)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})

# 세션 로컬 생성 (자동 커밋 및 자동 플러시 비활성화)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 클래스 생성을 위한 베이스 클래스
Base = declarative_base()
