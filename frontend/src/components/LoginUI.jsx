import React, { useState } from 'react';
import useLogin from '../hooks/useLogin';
import { useNavigate } from 'react-router-dom';
import InputField from './common/InputField';
import MessageDisplay from './common/MessageDisplay';
import './LoginUI.css';

// kakao 로그인 관련 상수
const REST_API_KEY = process.env.REACT_APP_KAKAO_REST_API_KEY;
const REDIRECT_URI = process.env.REACT_APP_KAKAO_REDIRECT_URI || "http://localhost:3000/oauth/callback/kakao";
const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`;


const LoginUI = ({ setIsAuthenticated, setIsSignup }) => {
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

      <InputField
        type="text"
        placeholder="Id"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <InputField
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <MessageDisplay message={error} isSuccess={false} />

      <button onClick={onLoginClick}>Login</button>

      {/* 카카오 로그인 버튼 */}
      <a href={KAKAO_AUTH_URL} className="kakao-login-button">
        <img
          src="/assets/kakao_login_medium_wide.png"
          alt="카카오 로고"
        />
      </a>

      <div className="signup-link">
        <a onClick={() => setIsSignup(true)}>Sign up</a>
      </div>
    </div>
  );
};

export default LoginUI;