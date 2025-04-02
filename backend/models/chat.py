from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db import Base

# 채팅 세션 모델 정의
class ChatSession(Base):
    __tablename__ = "chat_sessions"  # 데이터베이스 테이블 이름

    id = Column(Integer, primary_key=True, index=True)  # 기본 키
    user_id = Column(Integer, ForeignKey("users.id"))  # users 테이블의 id를 참조하는 외래 키
    created_at = Column(DateTime, default=datetime.utcnow)  # 세션 생성 시간 (기본값: 현재 시간)

    user = relationship("User", back_populates="chat_sessions")  # User 모델과의 관계 설정
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")  
    # ChatMessage 모델과의 관계 설정, 세션 삭제 시 메시지도 함께 삭제

# 채팅 메시지 모델 정의
class ChatMessage(Base):
    __tablename__ = "chat_messages"  # 데이터베이스 테이블 이름

    id = Column(Integer, primary_key=True, index=True)  # 기본 키
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))  # chat_sessions 테이블의 id를 참조하는 외래 키
    sender = Column(String)  # 메시지 발신자 ("user" 또는 "bot")
    message = Column(Text)  # 메시지 내용
    timestamp = Column(DateTime, default=datetime.utcnow)  # 메시지 생성 시간 (기본값: 현재 시간)

    session = relationship("ChatSession", back_populates="messages")  # ChatSession 모델과의 관계 설정

# User 모델에 chat_sessions 관계 추가 (user.py 모델과 연관 필요)
from models.user import User
User.chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
# User 모델에 ChatSession과의 관계를 설정, 사용자 삭제 시 관련 세션도 함께 삭제