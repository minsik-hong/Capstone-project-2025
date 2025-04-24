from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chatbot_test import run_chatbot  # run_qa에서 분리된 함수

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    source: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = run_chatbot(request.question)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
