// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import ChatbotPage from './pages/ChatbotPage';
import LoginPage from './pages/LoginPage';
import KakaoCallback from './pages/KakaoCallback';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // access_token 있는지 확인해서 자동 로그인 처리
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <Router basename="/">
      <Routes>
        <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
        
        {/* 카카오 리다이렉트 처리용 경로 */}
        <Route path="/oauth/callback/kakao" element={<KakaoCallback />} />

        {isAuthenticated ? (
          <>
            <Route path="/chatbot" element={<ChatbotPage />} />
            <Route path="*" element={<Navigate to="/chatbot" />} />
          </>
        ) : (
          <Route path="*" element={<Navigate to="/login" />} />
        )}
      </Routes>
    </Router>
  );
};

export default App;