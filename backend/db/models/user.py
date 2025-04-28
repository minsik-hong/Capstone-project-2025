# #데이터베이스 테이블을 정의하는 파일

# from sqlalchemy import Column, Integer, String
# from db.base import Base

# #users 테이블에 해당하는 구조를 정의
# class User(Base):
#     __tablename__ = "users"
#      # 자동 증가하는 id 컬럼을 Primary Key로 설정
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)

#데이터베이스 테이블을 정의하는 파일

from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    provider = Column(String(20), default="local")  # local, google 등
    
    
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(UUID, default=uuid.uuid4, unique=True, nullable=False)
    started_at = Column(TIMESTAMP, nullable=False)
    summary = Column(Text)

    messages = relationship("ChatSessionMessage", back_populates="session")

class ChatSessionMessage(Base):
    __tablename__ = "chat_session_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID, ForeignKey("chat_sessions.session_id"), nullable=False)
    sender = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    message_metadata = Column(JSONB, nullable=True) #선택사항항
    created_at = Column(TIMESTAMP, nullable=False)
    
    session = relationship("ChatSession", back_populates="messages")