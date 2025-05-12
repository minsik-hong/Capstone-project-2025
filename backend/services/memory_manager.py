# backend/services/memory_manager.py

from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from db.models.chat import ChatSession, ChatSessionMessage
from langchain.schema import AIMessage, HumanMessage
from datetime import datetime
from uuid import UUID

class UserSessionMemoryManager:
    def __init__(self, db: Session, session_id: str, user_id: str):
        self.db = db
        self.session_id = UUID(session_id)
        self.user_id = user_id

        # 세션 생성
        session = self.db.query(ChatSession).filter(ChatSession.session_id == self.session_id).first()
        if session is None:
            session = ChatSession(session_id=self.session_id, user_id=UUID(user_id), started_at=datetime.utcnow())
            self.db.add(session)
            self.db.commit()

        self.session = session

        # GPT 요약 메모리로 변경
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True
        )

        self._load_history()

    def _load_history(self):
        messages = (
            self.db.query(ChatSessionMessage)
            .filter(ChatSessionMessage.session_id == self.session_id)
            .order_by(ChatSessionMessage.created_at)
            .all()
        )

        for msg in messages:
            if msg.sender == "user":
                self.memory.chat_memory.add_message(HumanMessage(content=msg.message))
            else:
                self.memory.chat_memory.add_message(AIMessage(content=msg.message))

    def save_message(self, sender: str, message: str):
        msg = ChatSessionMessage(
            session_id=self.session_id,
            sender=sender,
            message=message,
            created_at=datetime.utcnow(),
        )
        self.db.add(msg)
        self.db.commit()

        if sender == "user":
            self.memory.chat_memory.add_message(HumanMessage(content=message))
        else:
            self.memory.chat_memory.add_message(AIMessage(content=message))

    def get_memory(self):
        return self.memory