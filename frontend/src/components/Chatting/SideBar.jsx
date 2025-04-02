import React from "react";
import ChatItem from "./ChatItem";
import "./SideBar.css";

function Sidebar() {
  const chatHistory = [
    { id: 1, title: "Chat1" },
    { id: 2, title: "Chat2" },
  ];

  return (
    <div className="sidebar">
      <div className="nav-container">
        <div className="profile-section">
          <div className="profile-picture"></div>
          <div className="profile-name">Name</div>
        </div>
        <div className="news-tags">
          <button className="tag-button">#CNN</button>
          <button className="tag-button">#BBC</button>
        </div>
        <div className="new-chat-container">
          <button className="new-chat-button">+ New Chat</button>
        </div>
        <div className="chat-history">
          <div className="chat-history-header">
            <h2 className="chat-title">Chats</h2>
            <hr className="chat-divider" />
            <p className="chat-date">날짜</p>
          </div>
          {chatHistory.map((chat) => (
            <ChatItem key={chat.id} title={chat.title} onClick={() => console.log(chat.id)} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default Sidebar;