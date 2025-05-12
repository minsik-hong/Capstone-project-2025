
from .login_attempt import LoginAttempt
from .user import User, UserProfile
from .chat import ChatSession, ChatSessionMessage
from sqlalchemy.orm import relationship

# SQLAlchemy 모델 간의 관계 설정

# User <-> ChatSession (1:N)
# 한 사용자는 여러 개의 채팅 세션을 가질 수 있음
User.chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
ChatSession.user = relationship("User", back_populates="chat_sessions")

# ChatSession <-> ChatSessionMessage (1:N)
# 하나의 채팅 세션에는 여러 개의 메시지가 있음
ChatSession.messages = relationship("ChatSessionMessage", back_populates="session", cascade="all, delete-orphan")
ChatSessionMessage.session = relationship("ChatSession", back_populates="messages")

# User <-> UserProfile (1:1)
# 한 사용자는 하나의 학습 성향 프로필을 가질 수 있음
User.profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
UserProfile.user = relationship("User", back_populates="profile")