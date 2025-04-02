import React from "react";
import "./Canvas.css";

/**
 * Canvas 컴포넌트
 * props:
 *  - text: 박스에 표시될 텍스트
 *  - onOpen: Canvas 창 열기 핸들러
 */
function Canvas({ text, onOpen }) {
  const imageSrc = "/assets/document-icon.svg";

  return (
    <div className="canvas-box" onClick={onOpen}>
      <img src={imageSrc} alt="" className="canvas-icon" />
      <span className="canvas-text">{text}</span>
    </div>
  );
}

export default Canvas;
