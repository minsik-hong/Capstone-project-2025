import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import ChatbotPage from './pages/ChatbotPage';
import NewsPage from './pages/NewsPage';
import LoginPage from './pages/LoginPage';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router basename="/">
      <Routes>
      <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />

        {
          isAuthenticated ? (
            <>
              <Route path="/" element={<Home />} />
              <Route path="/chatbot" element={<ChatbotPage />} />
              <Route path="/news" element={<NewsPage />} />
            </>
          ) : (<Route path="*" element={<Navigate to="/login" />} />)
        }
      </Routes>
    </Router>
  );
};

export default App;
