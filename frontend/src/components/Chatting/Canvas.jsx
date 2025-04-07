import React from "react";
import "./Canvas.css";

/**
 * Canvas 컴포넌트
 * props:
 *  - text: 뉴스 요약 텍스트
 *  - source: 뉴스 출처 URL
 *  - onOpen: Canvas 창 열기 핸들러
 */
function Canvas({ text, source, onOpen }) {
  const imageSrc = "/assets/document-icon.svg";

  return (
    <div className="canvas-box" onClick={onOpen}>
      <img src={imageSrc} alt="document" className="canvas-icon" />
      <div className="canvas-content">
        <span className="canvas-text">{text}</span>
        {source && (
          <a
            className="canvas-link"
            href={source}
            target="_blank"
            rel="noreferrer"
            onClick={(e) => e.stopPropagation()} // 박스 클릭과 분리
          >
            🔗 출처 보기
          </a>
        )}
      </div>
    </div>
  );
}

export default Canvas;
