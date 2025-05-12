// frontend/src/components/Chatting/ChatWindow.jsx
import React from 'react';
import ChatBubble from './ChatBubble';
import Canvas from './Canvas';
import './ChatWindow.css';

function ChatWindow({
  messages,
  userInput,
  setUserInput,
  sendMessage,
  messageEndRef,
  mode,
  setMode,
  onCanvasOpen,
  isCanvasOpen,
  quizStates,
  updateQuizState,
}) {
  const toggleMode = (selectedMode) => {
    setMode(mode === selectedMode ? "" : selectedMode);
  };

  return (
    <div className="chat-window">
      <div className={`chat-body ${isCanvasOpen ? 'reduced' : ''}`}>
        {messages.map((msg) => {
          if (msg.type === 'canvas') {
            return (
              <Canvas
                key={msg.id}
                text={msg.text}
                source={msg.source}
                mode={msg.mode}
                onOpen={() => onCanvasOpen(msg)}
                quizState={quizStates[msg.id] || { selectedAnswers: ["", "", ""], submitted: false }}
                updateQuizState={(updates) => updateQuizState(msg.id, updates)}
              />
            );
          } else if (msg.type === 'loading') {
            return (
              <div key={msg.id} className="chat-loading">
                <div className="spinner" />
                <p>답변을 생성 중입니다...</p>
              </div>
            );
          } else {
            return <ChatBubble key={msg.id} message={msg.text} sender={msg.sender} />;
          }
        })}
        <div ref={messageEndRef} />
      </div>

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