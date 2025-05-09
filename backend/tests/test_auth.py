import os
import pytest
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from models.user import User
from models.login_attempt import LoginAttempt
from services import auth  # auth.py가 services 폴더에 있다고 가정

# 테스트용 DB (SQLite 메모리 DB)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# JWT 설정을 위한 환경 변수 미리 세팅
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

# 테스트용 DB 초기화
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_register_user(db):
    user = auth.register_user(db, "test@example.com", "password123")
    assert user.email == "test@example.com"
    assert user.hashed_password != "password123"  # 해시화 확인


def test_authenticate_user_success(db):
    user = auth.authenticate_user(db, "test@example.com", "password123")
    assert user is not None
    assert user.email == "test@example.com"


def test_authenticate_user_wrong_email(db):
    user = auth.authenticate_user(db, "wrong@example.com", "password123")
    assert user is None


def test_authenticate_user_wrong_password(db):
    user = auth.authenticate_user(db, "test@example.com", "wrongpass")
    assert user is None


def test_password_hashing():
    raw = "securepass"
    hashed = auth.hash_password(raw)
    assert auth.verify_password(raw, hashed)
    assert not auth.verify_password("wrongpass", hashed)


def test_create_access_token():
    data = {"sub": "testuser@example.com"}
    token = auth.create_access_token(data, timedelta(minutes=5))
    assert isinstance(token, str)

    # JWT 디코드
    decoded = jwt.decode(
        token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms=["HS256"],
        audience="your-frontend",
        options={"verify_aud": False}  # 필요시 verify_aud 켜기
    )
    assert decoded["sub"] == "testuser@example.com"
    assert "exp" in decoded
    assert "iat" in decoded
