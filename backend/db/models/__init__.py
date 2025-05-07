# backend/db/models/__init__.py

from .user import User
from .chat import ChatSession, ChatSessionMessage
from sqlalchemy.orm import relationship

# 관계 선언

User.chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
ChatSession.user = relationship("User", back_populates="chat_sessions")

ChatSession.messages = relationship("ChatSessionMessage", back_populates="session", cascade="all, delete-orphan")
ChatSessionMessage.session = relationship("ChatSession", back_populates="messages")
