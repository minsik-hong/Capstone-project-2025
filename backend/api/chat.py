# backend/api/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chatbot_test import run_chatbot  # run_qa에서 분리된 함수
import traceback

from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    mode: Optional[str] = "default"

class ChatResponse(BaseModel):
    answer: str
    source: Optional[str] = None  # 없으면 None으로 가도 됨

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = run_chatbot(request.question, request.mode)
        # result = run_chatbot(request.question)
        return ChatResponse(**result)
    except Exception as e:
        traceback.print_exc()  # 내부 에러 확인
        print("Chat API Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

