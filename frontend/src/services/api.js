import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // 백엔드 API 기본 URL 설정

// 챗봇 응답 받기
export const fetchChatResponse = async (message) => {
  try {
    // 백엔드의 /chat 엔드포인트로 메시지를 전송하여 응답 받기
    const response = await axios.post(`${API_URL}/chat`, { message });
    return response.data.reply; // 응답 데이터에서 봇의 답변 반환
  } catch (error) {
    console.error('Chatbot API error:', error); // 에러 로그 출력
    return 'Sorry, something went wrong.'; // 에러 발생 시 기본 메시지 반환
  }
};

// 뉴스 가져오기
export const fetchNews = async () => {
  try {
    // 백엔드의 /news 엔드포인트에서 뉴스 데이터 가져오기
    const response = await axios.get(`${API_URL}/news`);
    return response.data.articles; // 응답 데이터에서 뉴스 기사 배열 반환
  } catch (error) {
    console.error('News API error:', error); // 에러 로그 출력
    return []; // 에러 발생 시 빈 배열 반환
  }
};

// 퀴즈 데이터 가져오기
export const fetchQuiz = async () => {
  try {
    // 백엔드의 /quiz 엔드포인트에서 퀴즈 데이터 가져오기
    const response = await axios.get(`${API_URL}/quiz`);
    return response.data; // 응답 데이터 반환
  } catch (error) {
    console.error('Quiz API error:', error); // 에러 로그 출력
    return []; // 에러 발생 시 빈 배열 반환
  }
};

// 사용자 로그인
export const loginUser = async (username, password) => {
  try {
    // 백엔드의 /users/login 엔드포인트로 로그인 요청
    const response = await axios.post(`${API_URL}/users/login`, { username, password });
    return response.data; // 응답 데이터 반환
  } catch (error) {
    console.error('Login API error:', error); // 에러 로그 출력
    return { success: false }; // 에러 발생 시 실패 상태 반환
  }
};

// 사용자 회원가입
export const registerUser = async (userData) => {
  try {
    // 백엔드의 /users/register 엔드포인트로 회원가입 요청
    const response = await axios.post(`${API_URL}/users/register`, userData);
    return response.data; // 응답 데이터 반환
  } catch (error) {
    console.error('Register API error:', error); // 에러 로그 출력
    return { success: false }; // 에러 발생 시 실패 상태 반환
  }
};