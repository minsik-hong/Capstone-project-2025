import React from 'react';
import ChatbotUI from '../components/ChatbotUI'; // Chatbot UI 컴포넌트 가져오기

// ChatbotPage 컴포넌트 정의
const ChatbotPage = () => (
  <div>
    <h2>AI Chatbot</h2> {/* 페이지 제목 */}
    <ChatbotUI /> {/* Chatbot UI 컴포넌트 렌더링 */}
  </div>
);

export default ChatbotPage; // ChatbotPage 컴포넌트 내보내기