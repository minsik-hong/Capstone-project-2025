# backend/db/models/user.py

from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from db.base import Base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
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
    provider = Column(String(20), default="local") # 로그인 확장
    level = Column(Enum(UserLevel), default=UserLevel.beginner)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    login_attempts = relationship("LoginAttempt", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', level='{self.level.value}')>"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    profile_level = Column(String, nullable=True)
    interests = Column(ARRAY(String), nullable=True)
    weaknesses = Column(ARRAY(String), nullable=True)
    summary = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 관계 설정
    user = relationship("User", back_populates="profile")

    @classmethod
    def upsert(cls, db: Session, user_id: UUID, profile_level: str, interests: list[str], weaknesses: list[str], summary: str):
        profile = db.query(cls).filter(cls.user_id == user_id).first()
        if profile:
            profile.level = profile_level
            profile.interests = interests
            profile.weaknesses = weaknesses
            profile.summary = summary
        else:
            profile = cls(
                user_id=user_id,
                profile_level=profile_level,
                interests=interests,
                weaknesses=weaknesses,
                summary=summary,
            )
            db.add(profile)
        db.commit()
        return profile

    @classmethod
    def get(cls, db: Session, user_id: UUID):
        return db.query(cls).filter(cls.user_id == user_id).first()