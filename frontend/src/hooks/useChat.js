import { useState } from 'react';
import { fetchChatResponse } from '../services/api'; // API 호출 함수 가져오기

// 채팅 관련 로직을 관리하는 커스텀 훅
const useChat = () => {
  // 메시지 상태 관리 (사용자와 봇의 메시지 저장)
  const [messages, setMessages] = useState([]);

  // 메시지 전송 함수
  const sendMessage = async (text) => {
    // 사용자 메시지 객체 생성
    const userMessage = { text, sender: 'user' };
    // 기존 메시지 배열에 사용자 메시지 추가
    setMessages((msgs) => [...msgs, userMessage]);

    // API를 통해 봇의 응답 가져오기
    const botResponse = await fetchChatResponse(text);
    // 봇의 응답 메시지를 기존 메시지 배열에 추가
    setMessages((msgs) => [...msgs, { text: botResponse, sender: 'bot' }]);
  };

  // 메시지 배열과 메시지 전송 함수를 반환
  return { messages, sendMessage };
};

export default useChat; // 커스텀 훅 내보내기