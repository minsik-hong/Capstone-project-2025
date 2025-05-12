import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./Canvas.css";
import MarkdownMessage from "../common/MarkdownMessage";
import { submitQuizAnswers } from '../../services/api';

function Canvas({
  text,
  source,
  mode,
  onOpen,
  quizState = { selectedAnswers: ["", "", ""], submitted: false },
  updateQuizState = () => {}
}) {
  const imageSrc = "/assets/document-icon.svg";

  const isQuiz = (mode === "vocab" || mode === "grammar") &&
    text?.match(/\d+\..*?\n[A-D]\)/);

  const formatMarkdownText = (rawText) => {
    return rawText
      .replace(/(\d+\..*?)\s+(?=[A-D]\))/g, "\n\n$1\n")
      .replace(/([A-D])\)/g, "\n$1)")
      .replace(/Answers:/g, "\n\n**Answers:**");
  };

  const formattedQuizText = formatMarkdownText(text);

  const extractQuestions = () => {
    const mainText = text.split(/Answers?:/)[0];
    return mainText
      .split(/\d+\.\s/)
      .slice(1)
      .map((q) => q.trim());
  };

  const questions = isQuiz ? extractQuestions() : [];

  const handleChoice = (index, choice) => {
    if (quizState.submitted) return;
    const updated = [...quizState.selectedAnswers];
    updated[index] = choice;
    updateQuizState({ selectedAnswers: updated });
  };

  const handleSubmit = async () => {
    if (quizState.selectedAnswers.some((s) => !s)) {
      alert("모든 문제에 답해주세요.");
      return;
    }
    updateQuizState({ submitted: true });

    //  콘솔 로그 추가 (중요)
    const userId = localStorage.getItem("user_id");
    const sessionId = localStorage.getItem("session_id"); // 또는 props에서 전달된 sessionId

     console.log("전송 데이터 확인", {
      user_id: userId,
      session_id: sessionId,
      quiz_content: text,
      user_answers: quizState.selectedAnswers
    });

    try {
      const feedback = await submitQuizAnswers(userId, sessionId, text, quizState.selectedAnswers);
      updateQuizState({ feedback: feedback.feedback });
    } catch (err) {
      console.error("퀴즈 제출 실패", err);
      alert("제출 중 오류가 발생했습니다.");
    }
  };

  return (
    <motion.div
      className="canvas-box"
      onClick={onOpen}
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 24 }}
      transition={{ duration: 0.35 }}
    >
      <motion.img
        src={imageSrc}
        alt="document"
        className="canvas-icon"
        initial={{ rotate: -6, scale: 0.9 }}
        animate={{ rotate: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 300, damping: 18 }}
      />
      <div className="canvas-content">
        <MarkdownMessage text={formattedQuizText} />

        {isQuiz && questions.map((_, idx) => (
            <div key={idx} className="choices">
              {["A", "B", "C", "D"].map((opt) => (
                <motion.button
                  key={opt}
                className={`choice-btn ${quizState.selectedAnswers[idx] === opt ? "selected" : ""}`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleChoice(idx, opt);
                  }}
                >
                  {opt}
                </motion.button>
              ))}
            </div>
          ))}

        {isQuiz && (
          <div className="canvas-submit">
            <AnimatePresence mode="wait">
              {!quizState.submitted ? (
                <motion.button
                  key="submit"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSubmit();
                  }}
                >
                  제출하기
                </motion.button>
              ) : (
                <motion.div
                  key="done"
                  className="submitted-msg"
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  ✅ 답안이 제출되었습니다.
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}

        {/* 피드백 출력 */}
        {quizState.feedback && (
          <motion.div
            className="quiz-feedback"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
          >
            <MarkdownMessage text={quizState.feedback} />
          </motion.div>
        )}

        {source && (
          <a
            className="canvas-link"
            href={source}
            target="_blank"
            rel="noreferrer"
            onClick={(e) => e.stopPropagation()}
          >
            🔗 출처 보기
          </a>
        )}
      </div>
    </motion.div>
  );
}

export default Canvas;