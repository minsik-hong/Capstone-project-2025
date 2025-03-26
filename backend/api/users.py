from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.session import SessionLocal
from db.models.user import User
from db.schemas.user import UserCreate, UserLogin
from services.auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

# 데이터베이스 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 회원가입 API
@router.post("/users/register")
def register(user: UserCreate, db: Session = Depends(get_db)): #get_db() 함수를 통해 DB 세션을 가져옴
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
    
    #새로운 유저 정보를 DB에 저장장
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # **회원가입 후 사용자 정보 반환 개선**
    return {"message": "User created successfully", "user": {"username": new_user.username, "email": new_user.email}}

#로그인 API
@router.post("/users/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # DB에서 사용자 정보를 가져옴
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # 사용자 정보가 없거나 비밀번호가 일치하지 않으면 오류 발생
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # JWT 토큰 생성
    access_token = create_access_token({"sub": db_user.username}, expires_delta=timedelta(minutes=30))
    
    # 토큰을 반환
    return {"access_token": access_token, "token_type": "bearer"}

