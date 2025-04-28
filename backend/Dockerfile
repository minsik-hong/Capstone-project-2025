FROM python:3.10

WORKDIR /app

# pip 최신화
RUN pip install --upgrade pip

# 🔹 PyTorch (CPU) 관련 패키지 먼저 설치 (캐시 유지 목적)
RUN pip install torch==2.2.2+cpu torchvision==0.17.2+cpu torchaudio==2.2.2+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html

# requirements.txt 복사
COPY requirements.txt .
# requirements.txt에 포함된 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 앱 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
