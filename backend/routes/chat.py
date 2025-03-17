from fastapi import APIRouter  # FastAPI의 라우터를 생성하기 위한 APIRouter 가져오기
from services.chatbot import chatbot_response  # 챗봇 응답을 처리하는 서비스 함수 가져오기

router = APIRouter()  # 새로운 라우터 인스턴스 생성

@router.post("/")  # HTTP POST 요청을 처리하는 엔드포인트 정의
def chat(user_query: str):
    """사용자의 질문을 받고, RAG 기반 뉴스 챗봇 응답을 반환"""
    response = chatbot_response(user_query)  # 사용자 질문을 챗봇 서비스에 전달하여 응답 생성
    return {"response": response}  # 생성된 응답을 JSON 형식으로 반환