// frontend/src/hooks/useLogin.js
import { useState } from 'react';
import { loginUser } from '../services/api'; // API 호출 함수 가져오기

const useLogin = () => {
  const [error, setError] = useState(null);

  const handleLogin = async (username, password) => {
    try {
      const result = await loginUser(username, password);
      if (result.access_token && result.user_id) {
        localStorage.setItem("token", result.access_token);     //  토큰 저장
        localStorage.setItem("user_id", result.user_id);        //  유저 ID 저장
        return true;
      } else {
        setError(result.message || '로그인에 실패했습니다.');
        return false;
      }
    } catch (err) {
      console.error(err);
      setError('로그인 중 오류가 발생했습니다.');
      return false;
    }
  };

  return { error, handleLogin };
};

export default useLogin;