from fastapi import APIRouter
from services.quiz_generator import generate_quiz

router = APIRouter()

@router.post("/")
def create_quiz(news_text: str):
    """뉴스 기사를 기반으로 퀴즈 생성"""
    quiz = generate_quiz(news_text)
    return {"quiz": quiz}
