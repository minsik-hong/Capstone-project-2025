import React, { useState } from "react";
import "./SettingsModal.css";
import MemoryManagerModal from "./MemoryManagerModal";

export default function SettingsModal({
  trigger,
  currentEmail = "user@example.com",
}) {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState("profile");
  const [newEmail, setNewEmail] = useState("");
  const [showManager, setShowManager] = useState(false);

  return (
    <>
      {/* ── 트리거(아이콘) ── */}
      <span onClick={() => setOpen(true)}>{trigger}</span>

      {/* ── 모달 ── */}
      {open && (
        <div className="modal-overlay" onClick={() => setOpen(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            {/* ========== 좌측 탭 목록 ========== */}
            <nav className="modal-aside">
              <button
                className={tab === "profile" ? "tab-btn active" : "tab-btn"}
                onClick={() => setTab("profile")}
              >
                프로필
              </button>
              <button
                className={tab === "memory" ? "tab-btn active" : "tab-btn"}
                onClick={() => setTab("memory")}
              >
                메모리
              </button>
            </nav>

            {/* ========== 우측 내용 영역 ========== */}
            <section className="modal-main">
              {/* ─ 프로필 탭 ─ */}
              {tab === "profile" && (
                <div className="profile-pane">
                  <h3>이메일 변경</h3>

                  <label className="field">
                    <span className="field-label">현재 이메일</span>
                    <span>{currentEmail}</span>
                  </label>

                  <label className="field">
                    <span className="field-label">새 이메일</span>
                    <input
                      type="email"
                      placeholder="example@domain.com"
                      value={newEmail}
                      onChange={(e) => setNewEmail(e.target.value)}
                    />
                  </label>

                  <div className="action-row">
                    <button className="save-btn" disabled>
                      저장 (미구현)
                    </button>
                  </div>
                </div>
              )}

              {/* ─ 메모리 탭 ─ */}
              {tab === "memory" && (
                <div className="memory-pane">
                  <h3>메모리 설정</h3>

                  <div className="toggle-row">
                    <div className="toggle-text">
                      <strong>저장된 메모리 참고</strong>
                      <p>응답할 때 메모리를 저장하고 사용하도록 합니다.</p>
                    </div>
                    <label className="switch">
                      <input type="checkbox" disabled />
                      <span className="slider"></span>
                    </label>
                  </div>
                  
                  {/* ─ 메모리 관리하기 링크 ─ */}
                  <div className="manage-link-row">
                    <button
                      className="manage-memory-link"
                      onClick={() => setShowManager(true)}
                    >
                      메모리 관리하기
                    </button>
                  </div>

                  <div className="toggle-row">
                    <div className="toggle-text">
                      <strong>채팅 기록 참고</strong>
                      <p>응답할 때 이전 모든 대화를 참고하도록 합니다.</p>
                    </div>
                    <label className="switch">
                      <input type="checkbox" disabled />
                      <span className="slider"></span>
                    </label>
                  </div>

                  {/* ─ 관리 모달 호출 ─ */}
                  {showManager && (
                    <MemoryManagerModal onClose={() => setShowManager(false)} />
                  )}
                </div>
              )}
            </section>

            {/* ─ 닫기 버튼 (우상단) ─ */}
            <button className="close-btn" onClick={() => setOpen(false)}>
              ×
            </button>
          </div>
        </div>
      )}
    </>
  );
}