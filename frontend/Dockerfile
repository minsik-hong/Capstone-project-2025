# React 빌드용 Node 이미지
FROM node:18

# 앱 디렉토리 생성 및 설정
WORKDIR /app

# 의존성 설치
COPY package*.json ./
RUN npm install

# 앱 소스 복사
COPY . .

# 앱 빌드
RUN npm run build

# 정적 파일 서빙용 웹서버 (serve)
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
