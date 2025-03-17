# 공통 의존성

from db import get_db  # 데이터베이스 세션을 가져오는 함수 가져오기
from services.vector_db import VectorDB  # 벡터DB 클래스 가져오기

# DB 종속성
def get_database():
    """데이터베이스 세션을 생성하고 반환"""
    db = get_db()  # 데이터베이스 세션 생성
    try:
        yield db  # 세션을 호출자에게 반환
    finally:
        db.close()  # 작업 완료 후 세션 닫기

# 벡터DB 인스턴스 생성
vector_db = VectorDB()  # 벡터DB 초기화