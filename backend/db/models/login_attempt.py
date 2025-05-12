from sqlalchemy import Column, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from db import Base

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    attempt_time = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, nullable=False)

    # 관계 설정: LoginAttempt -> User
    user = relationship("User", back_populates="login_attempts")
