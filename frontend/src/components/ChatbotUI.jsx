// frontend/src/components/common/ChatbotUI.jsx
import React, { useState } from 'react';
import Sidebar from './Chatting/SideBar';
import ChatWindow from './Chatting/ChatWindow';
import MarkdownMessage from './common/MarkdownMessage';
import Canvas from './Chatting/Canvas';
import './ChatbotUI.css';
import useChat from '../hooks/useChat';

function ChatbotUI() {
  const [selectedCanvas, setSelectedCanvas] = useState(null);
  const [quizStates, setQuizStates] = useState({});  // 메시지별 퀴즈 상태 저장
  const chat = useChat();

  const handleCanvasOpen = (canvas) => setSelectedCanvas(canvas);
  const handleCanvasClose = () => setSelectedCanvas(null);

  const updateQuizState = (msgId, updates) => {
    setQuizStates((prev) => ({
      ...prev,
      [msgId]: {
        ...prev[msgId],
        ...updates,
      },
    }));
  };

  const isCanvasOpen = Boolean(selectedCanvas);

  return (
    <div className="chat-container">
      <Sidebar />
      <ChatWindow
        {...chat}
        onCanvasOpen={handleCanvasOpen}
        isCanvasOpen={isCanvasOpen}
        quizStates={quizStates}
        updateQuizState={updateQuizState}
      />

      {isCanvasOpen && (
        <div className="canvas-panel">
          {/* 종료 버튼 */}
          <button
            className="close-btn"
            style={{
              position: "absolute",
              top: "16px",
              right: "16px",
              zIndex: 10,
              padding: "6px 10px",
              fontSize: "16px",
            }}
            onClick={handleCanvasClose}
          >
            ✖
          </button>

          {/* 퀴즈 모드일 경우 퀴즈 렌더링 */}
          {["vocab", "grammar"].includes(selectedCanvas?.mode) ? (
            <Canvas
              text={selectedCanvas.text}
              source={selectedCanvas.source}
              mode={selectedCanvas.mode}
              onOpen={() => {}}
              quizState={quizStates[selectedCanvas.id] || { selectedAnswers: ["", "", ""], submitted: false }}
              updateQuizState={(updates) => updateQuizState(selectedCanvas.id, updates)}
            />
          ) : (
            <>
              <div className="canvas-text" style={{ marginTop: "50px" }}>
                <MarkdownMessage text={selectedCanvas?.text} />
              </div>
              {selectedCanvas?.source && (
                <a
                  href={selectedCanvas.source}
                  target="_blank"
                  rel="noreferrer"
                  style={{ marginTop: "12px", display: "inline-block" }}
                >
                  🔗 출처 보기
                </a>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default ChatbotUI;