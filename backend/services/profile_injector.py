# backend/services/profile_injector.py
# 요약된 profile -> system prompt 삽입

from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def build_system_prompt(profile: dict) -> str:
    """
    사용자 프로필 dict를 받아 system prompt 문자열 생성
    """
    return f"""
You are tutoring a user with the following profile:

- English Level: {profile.get('level', 'Unknown')}
- Interests: {', '.join(profile.get('interests', []))}
- Weaknesses: {', '.join(profile.get('weaknesses', []))}

Adapt your explanations and tone to suit the learner's level and needs.
"""

def inject_profile_into_prompt(profile: dict) -> ChatPromptTemplate:
    """
    사용자 프로필을 LangChain ChatPromptTemplate에 삽입
    """
    system_prompt = build_system_prompt(profile)

    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
