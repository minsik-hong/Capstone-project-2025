import React, { useState } from 'react';
import LoginUI from '../components/LoginUI';
import SignupUI from '../components/SignupUI';
import './LoginPage.css';

const LoginPage = ({ setIsAuthenticated }) => {
  const [isSignup, setIsSignup] = useState(false); // signup 상태 추가

  return (
    <div className="login-page">
      <div className="login-left">
        <h1>Welcome!</h1>
        <p>Here is 어쩌구저쩌구. 배경에 이미지를 넣을지</p>
      </div>
      
      <div className="login-right">
        {isSignup ? (
          <SignupUI setIsSignup={setIsSignup} />
        ) : (
          <LoginUI setIsAuthenticated={setIsAuthenticated} setIsSignup={setIsSignup} />
        )}
      </div>
    </div>
  );
};

export default LoginPage;