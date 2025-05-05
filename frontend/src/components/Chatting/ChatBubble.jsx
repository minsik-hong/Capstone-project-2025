import React from "react";
import "./ChatBubble.css";
import MarkdownMessage from "../common/MarkdownMessage"; // 마크다운 메시지 컴포넌트


/**
 * 재사용 가능한 채팅 말풍선 컴포넌트
 * props:
 *  - message: 말풍선에 표시될 메시지 텍스트
 *  - sender: 보낸 사람("assistant" | "user" 등)
 */
function ChatBubble({ message, sender }) {
  return (
    <div className={`chat-bubble ${sender}`}>
      {/* <p className="message-text">{message}</p> */}

      {/* 마크다운 메시지 컴포넌트 사용 */}
      <MarkdownMessage text={message} />  
    </div>
  );
}

export default ChatBubble;