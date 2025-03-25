import React, { useState } from 'react';
import useLogin from '../hooks/useLogin';
import { useNavigate } from 'react-router-dom';
import InputField from './common/InputField';
import MessageDisplay from './common/MessageDisplay';
import './LoginUI.css';

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

      <div className="signup-link">
        <a onClick={() => setIsSignup(true)}>Sign up</a>
      </div>
    </div>
  );
};

export default LoginUI;
