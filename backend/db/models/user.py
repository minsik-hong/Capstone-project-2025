# backend/db/models/user.py

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from db.base import Base
import enum
import uuid

# 사용자 레벨 열거형
class UserLevel(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    provider = Column(String(20), default="local")
    level = Column(Enum(UserLevel), default=UserLevel.beginner)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계는 __init__.py 에서 선언

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', level='{self.level.value}')>"
