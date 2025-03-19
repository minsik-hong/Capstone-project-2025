from fastapi import FastAPI
from routes import users
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def root():
    return {"message": "Backend is running"}