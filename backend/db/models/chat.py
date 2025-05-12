from sqlalchemy import Column, String, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from db import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    started_at = Column(TIMESTAMP, nullable=False)
    summary = Column(Text)

    messages = relationship("ChatSessionMessage", back_populates="session")


class ChatSessionMessage(Base):
    __tablename__ = "chat_session_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.session_id"), nullable=False)
    sender = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    # message_metadata = Column(JSONB, nullable=True)  # 필요한 경우 주석 해제
    created_at = Column(TIMESTAMP, nullable=False)
    
    session = relationship("ChatSession", back_populates="messages")