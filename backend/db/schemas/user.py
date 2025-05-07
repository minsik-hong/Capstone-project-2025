#데이터 검증과 직렬화를 위한 Pydantic 모델을 정의
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    # 사용자명: 3~20자, 알파벳, 숫자, 밑줄(_)만 허용
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr         # 이메일: 이메일 형식 검증 abc@xyz.com 형식이 아니면 422 에러
    Password: str = Field(min_length=8, max_length=128)      # 비밀번호: 최소 8자 이상

    
class UserLogin(BaseModel):
    username: str
    password: str