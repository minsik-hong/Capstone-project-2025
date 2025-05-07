// ChatWindow.jsx
import React, { useState } from 'react';
import ChatBubble from './ChatBubble';
import Canvas from './Canvas';
import useChat from '../../hooks/useChat';
import './ChatWindow.css';

function ChatWindow({ onCanvasOpen, isCanvasOpen }) {
  const {
    messages,
    userInput,
    setUserInput,
    sendMessage,
    messageEndRef,
    mode,
    setMode,
  } = useChat();

  const toggleMode = (selectedMode) => {
    setMode(mode === selectedMode ? "" : selectedMode);
  };

  return (
    <div className="chat-window">
      <div className={`chat-body ${isCanvasOpen ? 'reduced' : ''}`}>
        {messages.map((msg) =>
          msg.type === 'canvas' ? (
            <Canvas
              key={msg.id}
              text={msg.text}
              source={msg.source}
              onOpen={() => onCanvasOpen(msg)}
            />
          ) : (
            <ChatBubble key={msg.id} message={msg.text} sender={msg.sender} />
          )
        )}
        <div ref={messageEndRef} />
      </div>
      
      {/* 모드 표시 */}
      {mode && (
        <div className="current-mode">
          <strong>Current Mode:</strong> {mode}
        </div>
      )}

      <div className="chat-footer">
        <div className="footer-buttons">
          <button className={`footer-button ${mode === "summary" ? "active" : ""}`} onClick={() => toggleMode("summary")}>Summary</button>
          <button className={`footer-button ${mode === "vocab" ? "active" : ""}`} onClick={() => toggleMode("vocab")}>Vocab Quiz</button>
          <button className={`footer-button ${mode === "grammar" ? "active" : ""}`} onClick={() => toggleMode("grammar")}>Grammar Quiz</button>
          <button className={`footer-button ${mode === "dialogue" ? "active" : ""}`} onClick={() => toggleMode("dialogue")}>Dialogue</button>
        </div>
        <div className="input-container">
          <input
            type="text"
            className="chat-input"
            placeholder="Write your message"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage(userInput, mode)}
          />
          <button className="send-button" onClick={() => sendMessage(userInput, mode)}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
