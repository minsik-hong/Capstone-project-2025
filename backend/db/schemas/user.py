#데이터 검증과 직렬화를 위한 Pydantic 모델을 정의
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
