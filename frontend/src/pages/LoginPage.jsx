import React, { useState } from "react";
import { motion } from "framer-motion";
import LoginUI from "../components/LoginUI";
import SignupUI from "../components/SignupUI";
import "./LoginPage.css";

const LoginPage = ({ setIsAuthenticated }) => {
  const [isSignup, setIsSignup] = useState(false);

  return (
    <div className="login-page">
      {/* ───────── 왼쪽 영역 ───────── */}
      <motion.div
        className="login-left"
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0.8, 0.25, 1] }}
      >
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Welcome!
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.35 }}
        >
          Your AI English coach that feeds on today’s news: read, quiz, and level up daily.
        </motion.p>
      </motion.div>

      {/* ───────── 오른쪽 영역 ───────── */}
      <motion.div
        className="login-right"
        initial={{ opacity: 0, x: 40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0.8, 0.25, 1] }}
      >
        {isSignup ? (
          <SignupUI setIsSignup={setIsSignup} />
        ) : (
          <LoginUI
            setIsAuthenticated={setIsAuthenticated}
            setIsSignup={setIsSignup}
          />
        )}
      </motion.div>
    </div>
  );
};

export default LoginPage;