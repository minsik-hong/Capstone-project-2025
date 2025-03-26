import React from 'react';

const MessageDisplay = ({ message, isSuccess }) => {
  if (!message) return null;

  return (
    <div className={isSuccess ? 'signup-success' : 'login-error'}>
      {message}
    </div>
  );
};

export default MessageDisplay;