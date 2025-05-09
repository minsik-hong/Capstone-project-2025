// frontend/src/services/api.js
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

// [수정됨] 질문하기 (user_id, session_id 포함)
export const askQuestion = async (user_id, session_id, question, mode = "") => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, {
      user_id,
      session_id,
      question,
      mode
    });
    return response.data;
  } catch (error) {
    console.error('Chatbot API error:', error);
    return {
      answer: "오류가 발생했습니다. 다시 시도해주세요.",
      source: "출처 없음",
    };
  }
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

// 사용자 프로필 분석
export const refreshUserProfile = async (userId) => {
  try {
    const response = await axios.post(`${API_URL}/api/users/profile/refresh/${userId}`);
    return response.data;
  } catch (error) {
    console.error('User Profile Refresh Error:', error);
    throw error;
  }
};
