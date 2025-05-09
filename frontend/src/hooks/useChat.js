// frontend/src/hooks/useChat.js
import { useState, useEffect, useRef } from 'react';
import { askQuestion } from '../services/api';
import { v4 as uuidv4 } from 'uuid';

const useChat = () => {
  const [source, setSource] = useState(null);
  const [mode, setMode] = useState("");
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(uuidv4());
  const messageEndRef = useRef(null);

  const selectSource = (selectedSource) => setSource(selectedSource);
  const selectMode = (selectedMode) => setMode(selectedMode);

  //  New Chat 시작
  const startNewChat = () => {
    setSessionId(uuidv4());
    setMessages([]);
  };

  const sendMessage = async (text, currentMode) => {
    if (text.trim()) {
      const userId = localStorage.getItem('user_id');  // 로그인 시 저장된 user_id 사용

      const userMsg = { id: Date.now(), text, sender: 'user' };
      setMessages((msgs) => [...msgs, userMsg]);
      setUserInput('');

      const botReply = await askQuestion(userId, sessionId, text, currentMode);

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
    startNewChat,       //  추가
    sessionId,          //  추가
  };
};

export default useChat;
