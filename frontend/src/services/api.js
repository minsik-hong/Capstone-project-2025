import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// 회원가입
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/api/users/register`, userData);
    return response.data;
  } catch (error) {
    console.error('Register API error:', error);
    return { success: false, message: error.response?.data?.detail || "Registration failed" };
  }
};

// 로그인
export const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/api/users/login`, { username, password });
    return response.data;
  } catch (error) {
    console.error('Login API error:', error);
    return { success: false, message: error.response?.data?.detail || "Login failed" };
  }
};


// 실제 FastAPI 챗봇 API 연결 함수 추가
export const askQuestion = async (question, mode = "") => {
  // export const askQuestion = async (question) => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, { question, mode });
    // const response = await axios.post(`${API_URL}/api/chat`, { question});
    return response.data; // { answer, source }
  } catch (error) {
    console.error('Chatbot API error:', error);
    return {
      answer: "오류가 발생했습니다. 다시 시도해주세요.",
      source: "출처 없음",
    };
  }
};


// 뉴스 요약 임시 구현
// topic: 사용자가 입력한 주제, source: "CNN" 또는 "BBC"
export const fetchNewsSummary = async (topic, source) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(
        `News summary from ${source} about "${topic}" - Blah Blah.`
      );
    }, 800);
  });
};

// 카카오 로그인 (인가 코드로 로그인 요청)
export const kakaoLogin = async (code) => {
  try {
    const response = await axios.get(`${API_URL}/api/oauth/kakao?code=${code}`);
    return response.data;
  } catch (error) {
    console.error('Kakao Login API error:', error);
    throw error;
  }
};