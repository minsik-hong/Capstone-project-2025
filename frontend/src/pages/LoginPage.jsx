import React, { useState } from "react";
import { loginUser } from "../services/api";  // api.js에서 로그인 함수 가져오기
import { useNavigate } from "react-router-dom";  // 페이지 이동을 위해

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();  // 로그인 후 이동할 페이지 설정

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const credentials = { email, password };
      await loginUser(credentials.email, credentials.password);  // 백엔드 로그인 API 호출
      navigate("/home");  // 로그인 성공 후 Home 페이지로 이동
    } catch (err) {
      setError("로그인 실패: 이메일 또는 비밀번호를 확인하세요.");
    }
  };

  return (
    <div>
      <h2>로그인</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">로그인</button>
      </form>
      <p>계정이 없으신가요?</p>
      <button onClick={() => navigate("/register")}>회원가입</button>
    </div>
  );
};

export default LoginPage;
