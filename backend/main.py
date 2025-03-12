# FastAPI 서버 실행

from fastapi import FastAPI
from routes import news, users, chat, quiz

app = FastAPI(title="RAG 기반 영어 학습 서비스")

# 라우트 등록
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])

@app.get("/")
async def root():
    return {"message": "RAG 기반 영어 학습 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
