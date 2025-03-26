import React, { useState } from 'react';
import { registerUser } from '../services/api';
import InputField from './common/InputField';
import MessageDisplay from './common/MessageDisplay';
import './LoginUI.css';

const SignupUI = ({ setIsSignup }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  const onSignupClick = async () => {
    if (username.trim() && email.trim() && password.trim()) {
      const response = await registerUser({ username, email, password });
      if (response.success === false) {
        setMessage(response.message);
        setIsSuccess(false);
      } else {
        setMessage('User created successfully');
        setIsSuccess(true);
      }
    }
  };

  return (
    <div className="login-container">
      <h2>Sign Up</h2>

      <InputField
        type="text"
        placeholder="Id"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <InputField
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <InputField
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <MessageDisplay message={message} isSuccess={isSuccess} />

      <button onClick={onSignupClick}>Sign Up</button>

      <div className="signup-link">
        <a onClick={() => setIsSignup(false)}>Back to Login</a>
      </div>
    </div>
  );
};

export default SignupUI;