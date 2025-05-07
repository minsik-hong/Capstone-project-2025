# backend/db/models/chat.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
import uuid

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)

    # 관계는 __init__.py 에서 선언


class ChatSessionMessage(Base):
    __tablename__ = "chat_session_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.session_id"), nullable=False)
    sender = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계는 __init__.py 에서 선언
