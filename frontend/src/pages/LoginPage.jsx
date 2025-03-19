import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = ({ setIsAuthenticated }) => {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    if (id === 'test@example.com' && password === 'password') {
      setIsAuthenticated(true);
      navigate('/');
    } else {
      alert('Invalid id or password');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="id"
        value={id}
        onChange={(e) => setId(e.target.value)}
        placeholder="id"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginPage;
