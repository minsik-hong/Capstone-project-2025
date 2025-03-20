import React, { useState } from "react";
import { registerUser } from "../services/api"; // 회원가입 API 호출 함수
import { useNavigate } from "react-router-dom"; // 페이지 이동

const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // 페이지 이동

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      await registerUser(email, password); // 회원가입 API 호출
      alert("회원가입 성공! 로그인 페이지로 이동합니다.");
      navigate("/login"); // 회원가입 후 로그인 페이지로 이동
    } catch (err) {
      setError("회원가입 실패: 이미 존재하는 이메일이거나 다른 오류가 발생했습니다.");
    }
  };

  return (
    <div>
      <h2>회원가입</h2>
      <form onSubmit={handleRegister}>
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
        <div>
          <label>Confirm Password:</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">회원가입</button>
      </form>

      {/* 로그인 페이지로 돌아가기 */}
      <p>이미 계정이 있으신가요?</p>
      <button onClick={() => navigate("/login")}>로그인</button>
    </div>
  );
};

export default RegisterPage;
