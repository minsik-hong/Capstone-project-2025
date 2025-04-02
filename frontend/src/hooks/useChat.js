import { useState, useEffect, useRef } from 'react';
import { fetchChatResponse } from '../services/api';

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

  const sendMessage = async (text) => {
    if (text.trim()) {
      const userMsg = { id: Date.now(), text, sender: 'user' };
      setMessages((msgs) => [...msgs, userMsg]);
      setUserInput(''); // 입력창 초기화
      const botReply = await fetchChatResponse(text);
      const botMsg = { id: Date.now() + 1, text: botReply, sender: 'assistant' };
      setMessages((msgs) => [...msgs, botMsg]);
      messageEndRef.current?.scrollIntoView({ behavior: 'smooth' }); // 스크롤 이동
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