import React from 'react';

const InputField = ({ type, placeholder, value, onChange, onKeyDown }) => {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      onKeyDown={onKeyDown}
    />
  );
};

export default InputField;