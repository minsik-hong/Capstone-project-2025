from dotenv import load_dotenv
load_dotenv()  # .env 파일에서 환경 변수 로드
from fastapi import FastAPI,Request
from api import users, chat  # chat 라우터 추가
from db.session import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

app = FastAPI()

# 예외 처리기 추가
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
   
    custom_errors = []

    for error in exc.errors():
        loc = error.get("loc")  # 오류가 발생한 위치
        msg = error.get("msg")  # 오류 메시지
        field = loc[-1] if loc else "Unknown field"  # 오류가 발생한 필드 이름

        # 각 오류에 대해 커스터마이즈된 메시지를 작성
        if "username" in field:
            if "length" in msg:
                msg = "사용자명은 3자 이상 20자 이내여야 합니다."
            elif "regex" in msg:
                msg = "사용자명은 알파벳, 숫자, 공백만 포함할 수 있습니다."

        elif "password" in field:
            if "length" in msg:
                msg = "비밀번호는 최소 8자, 최대 128자여야 합니다."
            elif "regex" in msg:
                msg = "비밀번호는 숫자, 대소문자, 특수문자를 포함해야 합니다."

        elif "email" in field:
            if "email" in msg:
                msg = "이메일 주소가 잘못되었습니다."

        # 커스터마이즈된 메시지를 추가
        custom_errors.append({
            "field": field,
            "message": msg,
        })

    return JSONResponse(
        status_code=422,
        content={"detail": custom_errors},
    )


# 앱 시작 시 PostgreSQL에 테이블 자동 생성
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# CORS 설정 (프론트엔드와 통신 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(users.router, prefix="/api")  # 회원 관련 엔드포인트: /api/users/...
app.include_router(chat.router, prefix="/api")   # 챗봇 관련 엔드포인트: /api/chat

@app.get("/")
def root():
    return {"message": "Backend is running"}