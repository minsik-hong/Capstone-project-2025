// ✅ ChatWindow.jsx
import React from 'react';
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
  } = useChat();

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
      <div className={`chat-footer ${isCanvasOpen ? 'reduced' : ''}`}>
        <div className="footer-buttons">
          <button className="footer-button">#Quiz Mode</button>
          <button className="footer-button">#Roleplay Mode</button>
        </div>
        <div className="input-container">
          <input
            type="text"
            className="chat-input"
            placeholder="Write your message"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage(userInput)}
          />
          <button className="send-button" onClick={() => sendMessage(userInput)}>
            <img src="/assets/send-icon.svg" alt="Send" className="send-icon" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
