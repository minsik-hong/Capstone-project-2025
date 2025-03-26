#데이터베이스 테이블을 정의하는 파일

from sqlalchemy import Column, Integer, String
from db.base import Base

#users 테이블에 해당하는 구조를 정의
class User(Base):
    __tablename__ = "users"
     # 자동 증가하는 id 컬럼을 Primary Key로 설정
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)