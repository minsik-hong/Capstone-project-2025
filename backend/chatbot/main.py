from fastapi import FastAPI  # FastAPI 애플리케이션 생성 및 관리
from routes import news, users, chat, quiz  # 라우트 모듈 가져오기

app = FastAPI()

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

def initialize_database():
    """DB 구축을 위한 초기화 함수"""
    from db_builder.main import main as db_builder_main  # db_builder의 main 함수 가져오기
    db_builder_main()  # DB 구축 실행

if __name__ == "__main__":  # 스크립트가 직접 실행될 경우
    initialize_database()  # 서버 시작 전에 DB 초기화 실행
    import uvicorn  # ASGI 서버 실행을 위한 uvicorn 가져오기
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 서버 실행 (모든 호스트에서 접근 가능, 포트 8000)
