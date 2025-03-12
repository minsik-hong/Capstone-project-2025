from fastapi import APIRouter
from services.chatbot import chatbot_response

router = APIRouter()

@router.post("/")
def chat(user_query: str):
    """사용자의 질문을 받고, RAG 기반 뉴스 챗봇 응답을 반환"""
    response = chatbot_response(user_query)
    return {"response": response}
