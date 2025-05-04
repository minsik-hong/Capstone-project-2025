// ✅ ChatbotUI.jsx
import React, { useState } from 'react';
import Sidebar from './Chatting/SideBar';
import ChatWindow from './Chatting/ChatWindow';
import MarkdownMessage from './common/MarkdownMessage'; // 마크다운 메시지 컴포넌트
import './ChatbotUI.css';

function ChatbotUI() {
  const [selectedCanvas, setSelectedCanvas] = useState(null);

  const handleCanvasOpen = (canvas) => setSelectedCanvas(canvas);
  const handleCanvasClose = () => setSelectedCanvas(null);

  const isCanvasOpen = Boolean(selectedCanvas);

  return (
    <div className="chat-container">
      <Sidebar />
      <ChatWindow onCanvasOpen={handleCanvasOpen} isCanvasOpen={isCanvasOpen} />
      {isCanvasOpen && (
        <div className="canvas-panel">
          <button className="close-btn" onClick={handleCanvasClose}>
            ✖
          </button>

          {/* <p>{selectedCanvas?.text}</p> */}
          {/* 마크다운 메시지 컴포넌트 사용 */}
          <div className="canvas-text">
            <MarkdownMessage text={selectedCanvas?.text} /> 
          </div> 

          {selectedCanvas?.source && (
            <a href={selectedCanvas.source} target="_blank" rel="noreferrer">
              🔗 출처 보기
            </a>
          )}
        </div>
      )}
    </div>
  );
}

export default ChatbotUI;