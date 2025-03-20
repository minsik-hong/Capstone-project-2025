import axios from 'axios';

const API_URL = "http://localhost:8000";  // 백엔드 FastAPI 서버 주소

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// 회원가입 API
export const registerUser = async (email, password) => {
  try {
    const response = await api.post("/users/register", {
      email,
      password,
    });
    return response.data;  // 성공적인 응답
  } catch (error) {
    console.error("회원가입 실패:", error);
    throw error;
  }
};

// 로그인 API
export const loginUser = async (email, password) => {
  try {
    const response = await api.post("/users/login", {
      username: email,
      password,
    });
    const { access_token } = response.data;
    // 로그인 성공 시 JWT 토큰을 로컬 스토리지에 저장
    localStorage.setItem("token", access_token);
    return response.data;
  } catch (error) {
    console.error("로그인 실패:", error);
    throw error;
  }
};
// ../services/api.js

export const fetchChatResponse = async (userMessage) => {
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch chat response');
    }

    const data = await response.json();
    return data.response;  // 챗봇의 응답을 반환
  } catch (error) {
    console.error("Error fetching chat response:", error);
    return 'Error: Unable to fetch response'; // 에러 발생 시 기본 응답
  }
};

// 기존 함수들 (로그인, 회원가입 등)
// (중복된 함수 선언 제거)
