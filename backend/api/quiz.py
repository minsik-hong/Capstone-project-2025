# backend/api/quiz.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import get_db
from services.prompt_templates import PROMPTS
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import traceback
from db.models.user import UserProfile  # 프로필 모델 임포트
from services.profile_injector import inject_profile_into_prompt  # 프로필 주입 함수

router = APIRouter()

class QuizSubmitRequest(BaseModel):
    user_id: str
    # session_id: str  # 추가
    quiz_content: str   # 전체 퀴즈 마크다운 텍스트
    user_answers: list[str]  # 예: ["A", "B", "D"]

class QuizFeedback(BaseModel):
    feedback: str  # 마크다운 피드백 전체 텍스트

@router.post("/quiz/submit", response_model=QuizFeedback)
def submit_quiz(request: QuizSubmitRequest, db: Session = Depends(get_db)):
    try:
        # 사용자 프로필 조회
        profile_obj = UserProfile.get(db, user_id=request.user_id)
        profile_dict = {}
        if profile_obj:
            profile_dict = {
                "level": profile_obj.profile_level,
                "interests": profile_obj.interests or [],
                "weaknesses": profile_obj.weaknesses or [],
            }

        # 프롬프트 생성 (기본 템플릿에 프로필 주입)
        base_prompt = PROMPTS["answer_reveal"]
        final_prompt = inject_profile_into_prompt(profile_dict, base_prompt)

        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)
        chain = LLMChain(prompt=final_prompt, llm=llm)

        user_answers_str = "\n".join([f"{i+1}. {a}" for i, a in enumerate(request.user_answers)])
        prompt_input = {
            "quiz_content": request.quiz_content,
            "user_answers": user_answers_str,
        }

        result = chain.run(prompt_input)
        return {"feedback": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
