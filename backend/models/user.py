#데이터베이스 users 테이블을 정의하는 파일
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    provider = Column(String(20), default="local")  # local, google 등
    refresh_token = Column(String, nullable=True)  # 추가됨

    login_attempts = relationship("LoginAttempt", back_populates="user")