# backend/services/user_profile.py
# 사용자 대화 요약/분석 함수

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy.orm import Session
from db.models.chat import ChatSession, ChatSessionMessage
from db.models.user_profile import UserProfile
from datetime import datetime
import json
from uuid import UUID

# ========== LLM 세팅 ==========
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

# ========== 프롬프트 ==========
profile_prompt = PromptTemplate.from_template("""
You are analyzing English learning behavior of a user.
Given the messages below, analyze and classify the user's English level (A1 to C2), learning interests (topics), and weaknesses (grammar, vocabulary, etc).

Messages:
{messages}

Respond in JSON:
{{
  "level": "A1 ~ C2",
  "interests": ["topic1", "topic2"],
  "weaknesses": ["grammar issue", "vocabulary gap"],
  "summary": "short summary of the user's style or pattern"
}}
""")

profile_chain = LLMChain(llm=llm, prompt=profile_prompt)

# ========== 유저 메시지 기반 분석 및 저장 ==========
def summarize_user_profile(user_id: str, db: Session, max_messages: int = 100) -> dict:
    """
    최근 user 메시지를 기반으로 레벨, 관심사, 약점 요약 -> DB 저장
    """
    sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).all()
    messages = []

    for session in sessions:
        msgs = (
            db.query(ChatSessionMessage)
            .filter(ChatSessionMessage.session_id == session.session_id)
            .order_by(ChatSessionMessage.created_at)
            .all()
        )
        for m in msgs:
            if m.sender == "user":
                messages.append(m.message)

    recent_messages = messages[-max_messages:]
    combined_text = "\n".join(recent_messages)

    result = profile_chain.invoke({"messages": combined_text})
    profile_data = json.loads(result["text"])

    # DB에 upsert
    UserProfile.upsert(
        db=db,
        user_id=UUID(user_id),
        level=profile_data.get("level"),
        interests=profile_data.get("interests", []),
        weaknesses=profile_data.get("weaknesses", []),
        summary=profile_data.get("summary")
    )

    return profile_data