import React from 'react';
import ReactMarkdown from 'react-markdown';
import './MarkdownMessage.css';

function MarkdownMessage({ text }) {
  return (
    <div className="markdown-message">
      <ReactMarkdown>{text}</ReactMarkdown>
    </div>
  );
}

export default MarkdownMessage;