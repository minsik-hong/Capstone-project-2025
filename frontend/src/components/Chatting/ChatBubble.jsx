import React from "react";
import { motion } from "framer-motion";
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
    <motion.div
      className={`chat-bubble ${sender}`}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 12 }}
      transition={{ duration: 0.25 }}
    >
      {/* 마크다운 메시지 컴포넌트 사용 */}
      <MarkdownMessage text={message} />  
    </motion.div>
  );
}

export default ChatBubble;