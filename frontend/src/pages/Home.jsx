import React from 'react';
import { Link } from 'react-router-dom'; // 페이지 간 이동을 위한 Link 컴포넌트 가져오기

// Home 컴포넌트 정의
const Home = () => (
  <div>
    <h1>Welcome to the News Learning Platform</h1> {/* 플랫폼의 메인 제목 */}
    <nav> {/* 내비게이션 영역 */}
      <Link to="/news">News Learning</Link> {/* 뉴스 학습 페이지로 이동하는 링크 */}
      <Link to="/chatbot">AI Chatbot</Link> {/* AI 챗봇 페이지로 이동하는 링크 */}
    </nav>
  </div>
);

export default Home; // Home 컴포넌트 내보내기