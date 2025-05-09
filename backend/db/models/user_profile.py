# backend/db/models/user_profile.py
from sqlalchemy import Column, String, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db.session import Base
from sqlalchemy.orm import Session
import uuid

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level = Column(String, nullable=True)
    interests = Column(ARRAY(String), nullable=True)
    weaknesses = Column(ARRAY(String), nullable=True)
    summary = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    def upsert(cls, db: Session, user_id: UUID, level: str, interests: list[str], weaknesses: list[str], summary: str):
        profile = db.query(cls).filter(cls.user_id == user_id).first()
        if profile:
            profile.level = level
            profile.interests = interests
            profile.weaknesses = weaknesses
            profile.summary = summary
        else:
            profile = cls(
                user_id=user_id,
                level=level,
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