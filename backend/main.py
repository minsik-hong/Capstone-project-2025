from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from api import users, chat, quiz
from db.session import Base, engine

app = FastAPI()

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"[⏱️ 요청 시간] {request.method} {request.url.path} → {process_time:.3f}s")
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is running"}
