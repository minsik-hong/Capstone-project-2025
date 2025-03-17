import React, { useState, useEffect, useRef } from 'react';
import { fetchChatResponse } from '../services/api'; // API 호출 함수 가져오기

const ChatbotUI = () => {
  // 메시지 상태 관리 (사용자와 봇의 메시지 저장)
  const [messages, setMessages] = useState([]);
  // 입력 필드 상태 관리
  const [input, setInput] = useState('');
  // 메시지 목록 끝을 참조하기 위한 ref
  const messageEndRef = useRef(null);

  // 메시지 전송 처리 함수
  const handleSend = async () => {
    if (input.trim()) { // 입력값이 비어있지 않은 경우에만 실행
      const userMessage = { text: input, sender: 'user' }; // 사용자 메시지 객체 생성
      setMessages((msgs) => [...msgs, userMessage]); // 기존 메시지 배열에 사용자 메시지 추가
      setInput(''); // 입력 필드 초기화

      // API를 통해 봇의 응답 가져오기
      const botReply = await fetchChatResponse(input);
      setMessages((msgs) => [...msgs, { text: botReply, sender: 'bot' }]); // 봇의 응답 메시지 추가
    }
  };

  // 메시지가 추가될 때마다 스크롤을 맨 아래로 이동
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chatbot-container"> {/* 채팅 UI 전체 컨테이너 */}
      <div className="chatbot-messages"> {/* 메시지 표시 영역 */}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}> {/* 메시지 스타일링 (사용자/봇) */}
            {msg.text} {/* 메시지 텍스트 표시 */}
          </div>
        ))}
        <div ref={messageEndRef} /> {/* 스크롤을 위한 참조 요소 */}
      </div>
      <div className="chatbot-input"> {/* 입력 필드와 버튼 영역 */}
        <input
          type="text"
          value={input} // 입력 필드 값 바인딩
          onChange={(e) => setInput(e.target.value)} // 입력값 변경 시 상태 업데이트
          onKeyPress={(e) => e.key === 'Enter' && handleSend()} // Enter 키로 메시지 전송
          placeholder="Type your message here..." // 입력 필드 플레이스홀더
        />
        <button onClick={handleSend}>Send</button> {/* 메시지 전송 버튼 */}
      </div>
    </div>
  );
};

export default ChatbotUI; // 컴포넌트 내보내기