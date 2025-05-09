// frontend/src/components/Chatting/Canvas.jsx
import React from "react";
import "./Canvas.css";
import MarkdownMessage from "../common/MarkdownMessage";

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
      .replace(/\*\*/g, "")
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

  const handleSubmit = () => {
    if (quizState.selectedAnswers.some((s) => !s)) {
      alert("모든 문제에 답해주세요.");
      return;
    }
    updateQuizState({ submitted: true });
    console.log("제출됨:", quizState.selectedAnswers);
  };

  return (
    <div className="canvas-box" onClick={onOpen}>
      <img src={imageSrc} alt="document" className="canvas-icon" />
      <div className="canvas-content">
        <MarkdownMessage text={formattedQuizText} />

        {isQuiz && questions.map((_, idx) => (
          <div key={idx} className="choices">
            {["A", "B", "C", "D"].map((opt) => (
              <button
                key={opt}
                className={`choice-btn ${quizState.selectedAnswers[idx] === opt ? "selected" : ""}`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleChoice(idx, opt);
                }}
              >
                {opt}
              </button>
            ))}
          </div>
        ))}

        {isQuiz && (
          <div className="canvas-submit">
            {!quizState.submitted ? (
              <button onClick={(e) => { e.stopPropagation(); handleSubmit(); }}>
                제출하기
              </button>
            ) : (
              <div className="submitted-msg">✅ 답안이 제출되었습니다.</div>
            )}
          </div>
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
    </div>
  );
}

export default Canvas;
