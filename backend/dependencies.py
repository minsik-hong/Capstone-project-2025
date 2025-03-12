# 공통 의존성

from db import get_db
from services.vector_db import VectorDB

# DB 종속성
def get_database():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# 벡터DB
vector_db = VectorDB()
