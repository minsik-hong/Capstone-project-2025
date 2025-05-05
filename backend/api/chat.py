# backend/api/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chatbot_test import run_chatbot  # run_qa에서 분리된 함수
import traceback

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    mode: str = ""

class ChatResponse(BaseModel):
    answer: str
    source: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = run_chatbot(request.question, request.mode)
        return ChatResponse(**result)
    except Exception as e:
        traceback.print_exc()  # 내부 에러 확인
        print("Chat API Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

