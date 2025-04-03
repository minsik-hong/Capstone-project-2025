FROM python:3.10

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 기본 명령어 (FastAPI 서버 실행 예시, 필요 시 수정)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]