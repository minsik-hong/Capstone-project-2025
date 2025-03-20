import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import ChatbotPage from './pages/ChatbotPage';
import NewsPage from './pages/NewsPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage'; // 회원가입 페이지 추가

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router basename="/">
      <Routes>
        {/* 로그인 및 회원가입 경로 추가 */}
        <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* 로그인 성공 후 접근 가능한 페이지 */}
        {isAuthenticated ? (
          <>
            <Route path="/" element={<Home />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
            <Route path="/news" element={<NewsPage />} />
          </>
        ) : (
          <Route path="*" element={<Navigate to="/login" />} />
        )}
      </Routes>
    </Router>
  );
};

export default App;
