from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_users():
    return {"message": "User API is working!"}
