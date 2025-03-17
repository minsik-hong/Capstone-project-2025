import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import ChatbotPage from './pages/ChatbotPage';
import NewsPage from './pages/NewsPage';

const App = () => {
  return (
    <Router basename="/">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<ChatbotPage />} />
        <Route path="/news" element={<NewsPage />} />
      </Routes>
    </Router>
  );
};

export default App;
