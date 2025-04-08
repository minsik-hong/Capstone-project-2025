from fastapi import FastAPI
from api import users
from fastapi.middleware.cors import CORSMiddleware
from db.session import Base, engine

app = FastAPI()


# ✅ 앱 시작 시 PostgreSQL에 테이블 자동 생성
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# CORS 설정 (프론트엔드와 통신 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}