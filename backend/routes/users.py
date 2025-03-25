from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.database import SessionLocal
from models.user import User
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

# 회원가입 요청 모델
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# 로그인 요청 모델
class UserLogin(BaseModel):
    username: str
    password: str

# 회원가입 API
# @router.post("/users/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     hashed_password = hash_password(user.password)
#     new_user = User(username=user.username, email=user.email, password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User created successfully"}

# 로그인 API
# @router.post("/users/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=400, detail="Invalid username or password")

#     access_token = create_access_token({"sub": db_user.username}, expires_delta=timedelta(minutes=30))
#     return {"access_token": access_token, "token_type": "bearer"}


# 임시 회원가입 API
@router.post("/users/register")
def register(user: UserCreate):
    # "testuser"라는 username은 이미 존재한다고 가정
    if user.username == "testuser":
        raise HTTPException(status_code=400, detail="Username 'testuser' is already taken")
    
    hashed_password = hash_password(user.password)
    return {
        "message": "User created successfully",
        "username": user.username,
        "hashed_password": hashed_password  # 테스트 목적의 해싱 결과
    }

#임시 로그인 처리 API
@router.post("/users/login")
def login(user: UserLogin):
    
    print("Received login:", user.username, user.password)
    # 예를 들어, "testuser"와 "1234"가 입력되면 로그인 성공
    if user.username == "testuser" and user.password == "1234":
        access_token = create_access_token(
            {"sub": user.username},
            expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
