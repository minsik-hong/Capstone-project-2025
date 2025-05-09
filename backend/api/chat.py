# backend/api/chat.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import get_db
from services.memory_manager import UserSessionMemoryManager
from services.chatbot_test import PROMPTS
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import traceback
import os
from uuid import UUID
from typing import Optional

from services.chatbot_test import run_chatbot_personalized # 개인화

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    question: str
    mode: Optional[str] = "default"

class ChatResponse(BaseModel):
    answer: str
    source: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = run_chatbot_personalized(
            user_id=request.user_id,
            session_id=request.session_id,
            user_input=request.question,
            mode=request.mode,
            db=db
        )
        return ChatResponse(answer=result["answer"], source=result["source"])
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
