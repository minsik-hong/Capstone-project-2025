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

# 개인화 테스트
# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
#     try:
#         memory_manager = UserSessionMemoryManager(db, request.session_id, request.user_id)
#         memory = memory_manager.get_memory()

#         llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))
#         prompt = PROMPTS.get(request.mode, PROMPTS["default"])

#         # 입력 키 자동 추출
#         input_key = prompt.input_variables[0] if prompt.input_variables else "input"

#         chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
#         result = chain.invoke({input_key: request.question})  # key 맞춰서 전달

#         answer = result["text"]

#         memory_manager.save_message("user", request.question)
#         memory_manager.save_message("bot", answer)

#         return ChatResponse(answer=answer, source=None)

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

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
