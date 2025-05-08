# JWT 인증 및 암호화 (사용자의 비밀번호를 해시화하고, 로그인 시 JWT 토큰을 발급)
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user import User
from db.schemas.user import UserCreate, UserLogin


# JWT 토큰 설정
SECRET_KEY = "your_secret_key" # 보안상 환경 변수로 저장 추천
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

# JWT 토큰 생성
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
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

# 로그인 (사용자 인증)
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
