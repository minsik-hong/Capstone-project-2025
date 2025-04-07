import { useState, useEffect, useRef } from 'react';
import { askQuestion } from '../services/api'; // ✅ 수정된 API 함수 사용

const useChat = () => {
  const [source, setSource] = useState(null);
  const [mode, setMode] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([
    { id: 1, sender: 'assistant', text: "Hello, I'm your English Assistant! How can I help you?" },
    { id: 2, sender: 'user', text: "~~~User's Chat~~~" },
    { id: 3, sender: 'assistant', text: "Here is ~~~NEWS~~~" },
    { id: 4, sender: 'assistant', type: 'canvas', text: "NEW CANVAS" },
  ]); // 초기 메시지 유지
  const messageEndRef = useRef(null);

  const selectSource = (selectedSource) => {
    setSource(selectedSource);
  };

  const selectMode = (selectedMode) => {
    setMode(selectedMode);
  };

  // ✅ 메시지 전송 함수 수정
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = { id: Date.now(), text, sender: 'user' };
    setMessages((msgs) => [...msgs, userMsg]);
    setUserInput('');

    try {
      const res = await askQuestion(text); // ✅ FastAPI에 질문 전송
      const botMsg = {
        id: Date.now() + 1,
        text: res.answer,
        sender: 'assistant',
        source: res.source, // 출처 포함
        type: 'text', // 필요 시 canvas 로직에 type 활용
      };
      setMessages((msgs) => [...msgs, botMsg]);

      // canvas용 출처 따로 저장하고 싶을 때
      if (res.source && res.answer) {
        setSource({
          text: res.answer,
          url: res.source,
        });
      }

      messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      return botMsg; // 필요 시 ChatWindow에서 받아 Canvas 열기
    } catch (error) {
      const errorMsg = {
        id: Date.now() + 2,
        text: "오류가 발생했습니다. 다시 시도해주세요.",
        sender: 'assistant',
      };
      setMessages((msgs) => [...msgs, errorMsg]);
      return errorMsg;
    }
  };

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return {
    source,
    mode,
    userInput,
    messages,
    messageEndRef,
    setUserInput,
    selectSource,
    selectMode,
    sendMessage,
    setMessages,
    setSource,
    setMode,
  };
};

export default useChat;