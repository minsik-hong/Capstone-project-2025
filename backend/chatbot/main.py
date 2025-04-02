from fastapi import FastAPI  # FastAPI 애플리케이션 생성 및 관리
from routes import news, users, chat, quiz  # 라우트 모듈 가져오기

app = FastAPI(title="RAG 기반 영어 학습 서비스")  # FastAPI 애플리케이션 생성 및 제목 설정

# 라우트 등록
app.include_router(news.router, prefix="/news", tags=["News"])  # 뉴스 관련 라우트 등록
app.include_router(users.router, prefix="/users", tags=["Users"])  # 사용자 관련 라우트 등록
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])  # 챗봇 관련 라우트 등록
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])  # 퀴즈 관련 라우트 등록

@app.get("/")  # 루트 엔드포인트 정의
async def root():
    return {"message": "RAG 기반 영어 학습 API"}  # 기본 메시지 반환

def initialize_database():
    """DB 구축을 위한 초기화 함수"""
    from db_builder.main import main as db_builder_main  # db_builder의 main 함수 가져오기
    db_builder_main()  # DB 구축 실행

if __name__ == "__main__":  # 스크립트가 직접 실행될 경우
    initialize_database()  # 서버 시작 전에 DB 초기화 실행
    import uvicorn  # ASGI 서버 실행을 위한 uvicorn 가져오기
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 서버 실행 (모든 호스트에서 접근 가능, 포트 8000)
