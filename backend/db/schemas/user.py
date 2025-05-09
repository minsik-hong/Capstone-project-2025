from pydantic import BaseModel, EmailStr, model_validator, ValidationError
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @model_validator(mode='before')  # before는 필드 검증 전에 실행됨
    def validate_username(cls, values):
        username = values.get('username')
        
        # 사용자명 유효성 검사: 3~20자, 알파벳, 숫자, 공백을 제외한 특수문자 허용
        if not (3 <= len(username) <= 20):
            raise ValueError('사용자명은 3~20자 이내여야 합니다.')
        if not re.match(r'^[a-zA-Z0-9 ]*$', username):  # 공백과 알파벳, 숫자만 허용
            raise ValueError('사용자명은 알파벳, 숫자, 공백만 포함할 수 있습니다.')
        
        return values

    @model_validator(mode='before')
    def validate_password(cls, values):
        password = values.get('password')
        
        # 비밀번호 유효성 검사: 최소 8자, 최대 128자
        if not (8 <= len(password) <= 128):
            raise ValueError('비밀번호는 최소 8자, 최대 128자 여야 합니다.')
        
        return values

    @model_validator(mode='before')
    def check_fields(cls, values):
        email = values.get('email')
        username = values.get('username')
        password = values.get('password')
        
        # 추가적인 전반적인 검증을 여기에 넣을 수 있습니다
        return values
    
class UserLogin(BaseModel):
    username: str
    password: str