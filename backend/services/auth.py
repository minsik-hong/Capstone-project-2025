# JWT 인증 및 암호화 (사용자의 비밀번호를 해시화하고, 로그인 시 JWT 토큰을 발급)
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user import User
from models.login_attempt import LoginAttempt  # LoginAttempt 모델 임포트
from db.schemas.user import UserCreate, UserLogin
import os  # ✅ 추가: 환경 변수 사용
from dotenv import load_dotenv  # ✅ dotenv 로드
from uuid import UUID  # ✅ UUID 임포트

# ✅ .env 파일에서 환경 변수 로드
load_dotenv()

# ✅ 환경 변수에서 JWT 시크릿 키 불러오기
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set in the .env file")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해시화 및 검증
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해시화
def hash_password(password: str):
    return pwd_context.hash(password)

# 비밀번호 검증
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅login_attempt 관련 변경 사항: 로그인 시도 기록을 위한 함수
def record_login_attempt(db: Session, user_id: UUID, success: bool):
    attempt = LoginAttempt(
        user_id=user_id,
        success=success,
        attempt_time=datetime.utcnow()  # 현재 시간을 기록
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


# ✅ 변경: JWT 토큰 생성 - issuer, subject, issued-at, audience 추가 가능
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=15))

    # ✅ 토큰에 보안 관련 클레임 추가
    to_encode.update({
        "exp": expire,
        "iat": now,                 # 토큰 발급 시간
        "nbf": now,                 # 이 시간 이전에는 유효하지 않음
        "iss": "your-service-name", # 발급자
        "aud": "your-frontend",     # 대상자 (검증 시 사용 가능)
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 사용자 조회 (이메일로)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 회원가입
def register_user(db: Session, email: str, password: str):
    hashed_password = hash_password(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅login_attempt 관련 변경사항: 로그인 (사용자 인증)
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        record_login_attempt(db, user_id=None, success=False)  # 로그인 실패 기록
        return None
    if not verify_password(password, user.hashed_password):
        record_login_attempt(db, user_id=user.id, success=False)  # 비밀번호 틀림 기록
        return None

    record_login_attempt(db, user_id=user.id, success=True)  # 로그인 성공 기록
    return user
