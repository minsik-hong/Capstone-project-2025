from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.session import SessionLocal
from db.models.user import User
from db.models.login_attempt import LoginAttempt # LoginAttempt 모델 임포트
from db.schemas.user import UserCreate, UserLogin
from services.auth import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
import os
import requests
from jose import JWTError, jwt  # ✅ 토큰 디코딩을 위한 jose 라이브러리 추가
from dotenv import load_dotenv

load_dotenv()  # ✅ .env 환경 변수 로딩

router = APIRouter()

# JWT 설정 (재발급에 필요)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # ✅ .env에서 불러옴
ALGORITHM = "HS256"


# 데이터베이스 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 회원가입 API
@router.post("/users/register")
def register(user: UserCreate, db: Session = Depends(get_db)): 
    # DB에서 중복된 username 체크
    db_user = db.query(User).filter(User.username == user.username).first() 
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # DB에서 중복된 email 체크 
    db_email = db.query(User).filter(User.email == user.email).first()  
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    
    # 새로운 유저 정보를 DB에 저장
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 회원가입 후 사용자 정보 반환
    return {"message": "User created successfully", "user": {"username": new_user.username, "email": new_user.email}}

# 로그인 API
@router.post("/users/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # DB에서 사용자 정보를 가져옴
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # 로그인 성공 여부 기록을 위해 초기 설정
    login_attempt = LoginAttempt(
        user_id=db_user.id if db_user else None,  # 사용자 ID 기록 (없으면 None)
        attempt_time=datetime.utcnow(),  # 시도 시간
        success=False  # 초기 상태는 실패
    )

    # 사용자 정보 및 비밀번호 검증
    if db_user and verify_password(user.password, db_user.password):
        # 로그인 성공 시
        login_attempt.success = True
        db.add(login_attempt)  # 로그인 이력 기록
        db.commit()

        # JWT 토큰 생성
        access_token = create_access_token({"sub": db_user.username}, expires_delta=timedelta(minutes=30))

        # 토큰 반환
        return {"access_token": access_token, "token_type": "bearer"}

    else:
        # 로그인 실패 시
        db.add(login_attempt)  # 로그인 이력 기록
        db.commit()

        # 로그인 실패 예외 처리
        raise HTTPException(status_code=400, detail="Invalid username or password")


# ✅ 토큰 재발급 API
@router.post("/users/refresh")
def refresh_token(request: Request):
    """
    Authorization 헤더로 전달된 JWT 토큰을 디코딩하여 유저 정보가 유효하면 새 토큰 발급
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token: no subject")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 새 토큰 생성
    new_token = create_access_token({"sub": username}, expires_delta=timedelta(minutes=30))
    return {"access_token": new_token, "token_type": "bearer"}


# 카카오 로그인 API
KAKAO_CLIENT_ID = os.getenv("KAKAO_REST_KEY")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

@router.get("/oauth/kakao")
def kakao_login(code: str, db: Session = Depends(get_db)):
    # 카카오 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post(token_url, headers=headers, data=data)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail=f"카카오 토큰 요청 실패: {token_json}")

    # 사용자 정보 요청
    user_res = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_res.json()

    kakao_id = str(user_info.get("id"))
    email = user_info.get("kakao_account", {}).get("email", f"{kakao_id}@kakao.fake")
    username = f"kakao_{kakao_id}"

    # DB 사용자 확인 or 생성
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(    
            username=username, 
            email=email, 
            password="kakao_login_dummy",           # 카카오 로그인은 비밀번호가 필요 없지만, 필드상 비밀번호 설정
            provider="kakao"                        # 카카오 로그인 시 provider를 "kakao"로 설정    
            )
        db.add(user)
        db.commit()
        db.refresh(user)

    # JWT 발급
    token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
