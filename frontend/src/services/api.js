import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// 회원가입
export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/users/register`, userData);
    return response.data;
  } catch (error) {
    console.error('Register API error:', error);
    return { success: false, message: error.response?.data?.detail || "Registration failed" };
  }
};

// 로그인
export const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/users/login`, { username, password });
    return response.data;
  } catch (error) {
    console.error('Login API error:', error);
    return { success: false, message: error.response?.data?.detail || "Login failed" };
  }
};

// // 챗봇 응답 받기
// export const fetchChatResponse = async (message) => {
//   try {
//     const response = await axios.post(`${API_URL}/chat`, { message });
//     return response.data.reply;
//   } catch (error) {
//     console.error('Chatbot API error:', error);
//     return 'Sorry, something went wrong.';
//   }
// };

// 챗봇 응답 임시 구현
export const fetchChatResponse = async (message) => {
  try {
    // ...existing code for actual API call (if needed)...
    throw new Error("Backend is not connected"); // 임시로 오류 발생
  } catch (error) {
    console.error('Chatbot API error:', error);
    return `Error: ${error.message || 'Something went wrong.'}`; // 오류 메시지 반환
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