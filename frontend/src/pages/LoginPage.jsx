import React, { useState } from 'react';
import LoginUI from '../components/LoginUI';
import './LoginPage.css';

const LoginPage = ({ setIsAuthenticated }) => {
  return (
    <div className="login-page">
      <div className="login-left">
        <h1>Welcome!</h1>
        <p>Here is 어쩌구저쩌구. 배경에 이미지를 넣을지</p>
      </div>
      
      <div className="login-right">
        <LoginUI setIsAuthenticated={setIsAuthenticated} />
      </div>
    </div>
  );
};

export default LoginPage;