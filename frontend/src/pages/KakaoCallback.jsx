import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { kakaoLogin } from '../services/api';

const KakaoCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const code = new URL(window.location.href).searchParams.get("code");

    if (code) {
      (async () => {
        try {
          const data = await kakaoLogin(code); // access_token 등 받기
          
          if (data.access_token) {
            localStorage.setItem('token', data.access_token);
            navigate('/chatbot'); // 로그인 완료 후 이동
          } else {
            throw new Error("No access token");
          }
        } catch (err) {
          console.error("카카오 로그인 실패:", err);
          navigate('/login'); // 실패 시 로그인 페이지로
        }
      })();
    }
  }, []);

  return <div>카카오 로그인 처리 중입니다...</div>;
};

export default KakaoCallback;