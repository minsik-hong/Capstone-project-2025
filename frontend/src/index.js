import React from 'react';
import ReactDOM from 'react-dom'; // ReactDOM을 사용하여 React 컴포넌트를 DOM에 렌더링
import App from './App'; // App 컴포넌트 가져오기
import './styles/chatbot.css'; // 스타일 시트 가져오기

// React 애플리케이션 렌더링
ReactDOM.render(
  <React.StrictMode> {/* 애플리케이션에서 잠재적인 문제를 감지하기 위한 StrictMode */}
    <App /> {/* App 컴포넌트를 렌더링 */}
  </React.StrictMode>,
  document.getElementById('root') // index.html의 root 요소에 렌더링
);