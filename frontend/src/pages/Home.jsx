import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";  // 페이지 이동을 위해

const Home = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // 로컬 스토리지에서 JWT 토큰 확인
    const token = localStorage.getItem("token");
    if (!token) {
      // 토큰이 없으면 로그인 페이지로 리다이렉트
      navigate("/login");
    } else {
      // 토큰이 있으면 사용자 정보 요청 (예: /me 엔드포인트)
      setUser({ email: "user@example.com" });  // 예시로 사용자 이메일을 표시
    }
  }, [navigate]);

  return (
    <div>
      <h2>홈 페이지</h2>
      {user ? (
        <div>
          <p>환영합니다, {user.email}</p>
          <button onClick={() => { localStorage.removeItem("token"); navigate("/login"); }}>로그아웃</button>
        </div>
      ) : (
        <p>로그인 중...</p>
      )}
    </div>
  );
};

export default Home;
