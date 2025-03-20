from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth import hash_password, verify_password
from services.user_service import create_user, create_access_token
from ..database.user_infoDB import SessionLocal
from schemas.user import UserCreate
from models.user import User
from datetime import timedelta

router = APIRouter()

# 데이터베이스 세션 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 비밀번호 해싱
    hashed_password = hash_password(user.password)
    db_user = create_user(db, email=user.email, password=hashed_password, full_name=user.full_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created successfully!"}

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}