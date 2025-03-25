import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import ChatbotPage from './pages/ChatbotPage';
import LoginPage from './pages/LoginPage';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router basename="/">
      <Routes>
        <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
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
