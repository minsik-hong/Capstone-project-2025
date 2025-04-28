# 1단계: 빌드용 Node 이미지
FROM node:18 AS builder

# 앱 디렉토리 생성
WORKDIR /app

# 의존성 설치를 위한 파일만 복사 (캐시 사용 가능)
COPY package*.json ./

# 의존성 설치 (캐시 최대 활용)
RUN npm install

# 전체 소스 복사
COPY . .

# 앱 빌드
RUN npm run build

# 2단계: 정적 서버용 경량 이미지
FROM node:18-slim

# serve 설치
RUN npm install -g serve

# 작업 디렉토리 설정
WORKDIR /app

# 빌드 결과만 복사 (용량 최소화)
COPY --from=builder /app/build ./build

# 정적 파일 서빙
CMD ["serve", "-s", "build", "-l", "3000"]
