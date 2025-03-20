from sqlalchemy.orm import Session
from models.user import User
from services.auth import hash_password

# 회원가입
def create_user(db: Session, username: str, email: str, password: str):
    hashed_pw = hash_password(password)
    db_user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 사용자 조회
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
