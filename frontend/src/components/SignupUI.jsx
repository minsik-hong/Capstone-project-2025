import React, { useState } from 'react';
import { registerUser } from '../services/api';
import './LoginUI.css';

const SignupUI = ({ setIsSignup }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const onSignupClick = async () => {
    if (username.trim() && email.trim() && password.trim()) {
      const result = await registerUser({ username, email, password });
      if (result.success) {
        setSuccess(true);
        setError(null);
      } else {
        setError(result.message);
      }
    }
  };

  return (
    <div className="login-container">
      <h2>Sign Up</h2>
      {success ? (
        <div>
          <p>Signup successful!</p>
          <a onClick={() => setIsSignup(false)}>Go to Login</a>
        </div>
      ) : (
        <>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && <div className="login-error">{error}</div>}
          <button onClick={onSignupClick}>Sign Up</button>
          <div className="signup-link">
            <a onClick={() => setIsSignup(false)}>Back to Login</a>
          </div>
        </>
      )}
    </div>
  );
};

export default SignupUI;
