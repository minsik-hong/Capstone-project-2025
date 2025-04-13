from fastapi import APIRouter  # FastAPI의 라우터를 생성하기 위한 APIRouter 가져오기

router = APIRouter()  # 새로운 라우터 인스턴스 생성

@router.get("/")  # HTTP GET 요청을 처리하는 엔드포인트 정의
def read_users():
    return {"message": "User API is working!"}  # 사용자 API가 작동 중임을 알리는 메시지 반환