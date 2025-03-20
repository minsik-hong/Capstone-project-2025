from pydantic import BaseModel

# UserCreate: 사용자가 회원가입 시 입력할 데이터
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True  # SQLAlchemy 모델과 호환되도록 설정

# UserLogin: 사용자가 로그인 시 입력할 데이터
class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True  # SQLAlchemy 모델과 호환되도록 설정
