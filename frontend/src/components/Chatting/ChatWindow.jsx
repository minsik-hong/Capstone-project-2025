import React from "react";
import ChatBubble from "./ChatBubble";
import Canvas from "./Canvas";
import useChat from "../../hooks/useChat"; // useChat 훅 가져오기
import "./ChatWindow.css";

function ChatWindow({ onCanvasOpen, isCanvasOpen }) {
  const {
    messages,
    userInput,
    setUserInput,
    sendMessage,
    messageEndRef, // 추가
  } = useChat(); // useChat 훅 사용

  // ✅ 메시지 전송 후 canvas 열기
  const handleSend = async () => {
    if (!userInput.trim()) return;
    const botResponse = await sendMessage(userInput);

    // 출처와 요약이 있으면 캔버스 열기
    if (
      botResponse &&
      botResponse.sender === "assistant" &&
      botResponse.text &&
      botResponse.source &&
      onCanvasOpen
    ) {
      onCanvasOpen(botResponse);
    }
  };

  return (
    <div className="chat-window">
      {/* 채팅 메시지 표시 영역 */}
      <div className={`chat-body ${isCanvasOpen ? "reduced" : ""}`}>
        {messages.map((msg) =>
          msg.type === "canvas" ? (
            <Canvas
              key={msg.id}
              text={msg.text}
              onOpen={() => onCanvasOpen(msg)}
            />
          ) : (
            <ChatBubble key={msg.id} message={msg.text} sender={msg.sender} />
          )
        )}
        <div ref={messageEndRef} /> {/* 스크롤 이동을 위한 참조 */}
      </div>
      {/* 입력 영역 */}
      <div className={`chat-footer ${isCanvasOpen ? "reduced" : ""}`}>
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
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage(userInput);
            }}
          />
          <button className="send-button" onClick={() => sendMessage(userInput)}>
            <img
              src="/assets/send-icon.svg"
              alt="Send"
              className="send-icon"
            />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;