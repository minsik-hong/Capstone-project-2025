import React, { useState } from 'react';
import useLogin from '../hooks/useLogin';
import { useNavigate } from 'react-router-dom';
import './LoginUI.css';

const LoginUI = ({ setIsAuthenticated }) => {
  // 아이디/비밀번호 상태
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { error, handleLogin } = useLogin();
  const navigate = useNavigate();

  // 로그인 버튼 클릭 시
  const onLoginClick = async () => {
    if (username.trim() && password.trim()) {
      const success = await handleLogin(username, password);
      if (success) {
        setIsAuthenticated(true);
        navigate('/'); // 로그인 성공 시 Home 페이지로 이동
      }
    }
  };

  // Enter 키로 로그인 처리
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onLoginClick();
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>

      {/* 아이디 입력 */}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      {/* 비밀번호 입력 */}
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      {/* 에러 메시지 표시 */}
      {error && <div className="login-error">{error}</div>}

      {/* 로그인 버튼 */}
      <button onClick={onLoginClick}>Login</button>

      {/* 회원가입 링크 (임시) */}
      <div className="signup-link">
        <a href="#signup">Sign up</a>
      </div>
    </div>
  );
};

export default LoginUI;
