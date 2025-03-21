import { useState } from 'react';
import { loginUser } from '../services/api'; // API 호출 함수 가져오기

const useLogin = () => {
  const [error, setError] = useState(null);

  const handleLogin = async (username, password) => {
    try {
      const result = await loginUser(username, password);
      if (result.access_token) {
        console.log('로그인 성공!', result);
        setError(null);
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