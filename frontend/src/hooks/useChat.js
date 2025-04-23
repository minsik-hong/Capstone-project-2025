// ✅ useChat.js
import { useState, useEffect, useRef } from 'react';
import { askQuestion } from '../services/api';

const useChat = () => {
  const [source, setSource] = useState(null);
  const [mode, setMode] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);  // 초기 메시지 없음
  const messageEndRef = useRef(null);

  const selectSource = (selectedSource) => setSource(selectedSource);
  const selectMode = (selectedMode) => setMode(selectedMode);

  const sendMessage = async (text) => {
    if (text.trim()) {
      const userMsg = { id: Date.now(), text, sender: 'user' };
      setMessages((msgs) => [...msgs, userMsg]);
      setUserInput('');

      const botReply = await askQuestion(text);  // ✅ 백엔드 호출

      const canvasMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        type: 'canvas',
        text: botReply.answer,
        source: botReply.source
      };

      setMessages((msgs) => [...msgs, canvasMsg]);
      messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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
