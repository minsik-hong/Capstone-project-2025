import React, { useState } from 'react';
import { registerUser } from '../services/api';
import InputField from './common/InputField';
import MessageDisplay from './common/MessageDisplay';
import './LoginUI.css';

export default function SignupUI({ setIsSignup }) {
  const [username, setUsername] = useState('');
  const [email, setEmail]     = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors]   = useState({});
  const [message, setMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  const onSignupClick = async () => {
    // 1) 빈 값 검사
    const newErr = {};
    if (!username.trim()) newErr.username = '필수 입력입니다';
    if (!email.trim())    newErr.email    = '필수 입력입니다';
    if (!password.trim()) newErr.password = '필수 입력입니다';
    if (Object.keys(newErr).length) {
      setErrors(newErr);
      setMessage('');
      return;
    }

    // 2) API 호출 & 에러 처리
    try {
      await registerUser({ username, email, password });
      // 성공
      setIsSuccess(true);
      setMessage('회원가입이 완료되었습니다');
      setErrors({});
    } catch (err) {
      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        // 배열로 오는 Pydantic 오류 메시지들을 전부 합쳐서 전역 메시지로 표시
        const allMsgs = detail.map(e => e.msg).join(' / ');
        setMessage(allMsgs);
        setIsSuccess(false);
        setErrors({});
      }
      else if (typeof detail === 'string') {
        // HTTPException(detail="...") 형태
        setMessage(detail);
        setIsSuccess(false);
        setErrors({});
      }
      else {
        setMessage('알 수 없는 서버 오류가 발생했습니다');
        setIsSuccess(false);
        setErrors({});
      }
    }
  };

  return (
    <div className="login-container">
      <h2>Sign Up</h2>

      <InputField
        type="text"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      {errors.username && (
        <MessageDisplay message={errors.username} isSuccess={false} />
      )}

      <InputField
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      {errors.email && (
        <MessageDisplay message={errors.email} isSuccess={false} />
      )}

      <InputField
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      {errors.password && (
        <MessageDisplay message={errors.password} isSuccess={false} />
      )}

      {/* 전역 메시지 (배열 or 문자열) */}
      {message && (
        <MessageDisplay message={message} isSuccess={isSuccess} />
      )}

      <button onClick={onSignupClick}>Sign Up</button>

      <div className="signup-link">
        <a onClick={() => setIsSignup(false)}>Back to Login</a>
      </div>
    </div>
  );
}