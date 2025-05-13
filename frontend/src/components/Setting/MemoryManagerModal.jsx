import React from "react";
import "./MemoryManagerModal.css";

export default function MemoryManagerModal({ onClose }) {
  /* ─ 샘플 메모리 데이터 ─ */
  const memories = [
    "Example memory1...",
    "Example memory2...",
    "Example memory3...",
  ];

  return (
    <div className="mem-overlay" onClick={onClose}>
      <div className="mem-dialog" onClick={(e) => e.stopPropagation()}>
        {/* 헤더 */}
        <header>
          <h3>저장된 메모리</h3>
        </header>

        {/* 메모리 목록 */}
        <ul className="mem-list">
          {memories.map((m, i) => (
            <li key={i}>
              <span className="text">{m}</span>
              <button className="trash" aria-label="delete" disabled>
                🗑
              </button>
            </li>
          ))}
        </ul>

        {/* 푸터 */}
        <div className="mem-footer">
          <button className="delete-all" disabled>
            모두 삭제
          </button>
        </div>

        {/* 닫기 */}
        <button className="close-btn" onClick={onClose}>
          ×
        </button>
      </div>
    </div>
  );
}