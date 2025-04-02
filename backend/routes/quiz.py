from fastapi import APIRouter  # FastAPI의 라우터를 생성하기 위한 APIRouter 가져오기
from backend.services.quiz_generator import generate_quiz  # 퀴즈를 생성하는 서비스 함수 가져오기

router = APIRouter()  # 새로운 라우터 인스턴스 생성

@router.post("/")  # HTTP POST 요청을 처리하는 엔드포인트 정의
def create_quiz(news_text: str):
    """뉴스 기사를 기반으로 퀴즈 생성"""
    quiz = generate_quiz(news_text)  # 뉴스 기사를 입력으로 받아 퀴즈 생성
    return {"quiz": quiz}  # 생성된 퀴즈를 JSON 형식으로 반환