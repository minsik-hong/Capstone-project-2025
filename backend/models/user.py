from sqlalchemy import Column, Integer, String, DateTime, Enum  # SQLAlchemy에서 필요한 클래스 가져오기
from datetime import datetime  # 날짜 및 시간 처리를 위한 datetime 모듈
from backend.db import Base  # SQLAlchemy Base 클래스 가져오기
import enum  # 열거형(enum) 지원을 위한 모듈

# 사용자 레벨을 정의하는 열거형 클래스
class UserLevel(enum.Enum):
    beginner = "beginner"  # 초급 사용자
    intermediate = "intermediate"  # 중급 사용자
    advanced = "advanced"  # 고급 사용자

# 사용자 모델 정의
class User(Base):
    __tablename__ = "users"  # 데이터베이스 테이블 이름

    id = Column(Integer, primary_key=True, index=True)  # 기본 키
    username = Column(String, unique=True, index=True, nullable=False)  # 고유한 사용자 이름
    email = Column(String, unique=True, index=True, nullable=False)  # 고유한 이메일 주소
    hashed_password = Column(String, nullable=False)  # 해시된 비밀번호
    created_at = Column(DateTime, default=datetime.utcnow)  # 계정 생성 시간 (기본값: 현재 시간)
    level = Column(Enum(UserLevel), default=UserLevel.beginner)  # 사용자 레벨 (기본값: beginner)

    # 객체를 문자열로 표현하는 메서드
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', level='{self.level.value}')>"