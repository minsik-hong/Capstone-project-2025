import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
console.log('API_URL:', API_URL);

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

// 챗봇 응답 받기
export const fetchChatResponse = async (message) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, { message });
    return response.data.reply;
  } catch (error) {
    console.error('Chatbot API error:', error);
    return 'Sorry, something went wrong.';
  }
};