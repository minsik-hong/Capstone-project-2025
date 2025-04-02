import React from "react";
import "./ChatItem.css";

/**
 * ChatItem 컴포넌트
 * props:
 *  - title: 채팅 제목
 *  - onClick: 클릭 이벤트 핸들러
 */
function ChatItem({ title, onClick }) {
  return (
    <div className="chat-item" onClick={onClick}>
      <img
        src="/assets/chat-icon.svg"
        alt="Chat Icon"
        className="chat-icon"
      />
      <div className="chat-title">{title}</div>
    </div>
  );
}

export default ChatItem;
