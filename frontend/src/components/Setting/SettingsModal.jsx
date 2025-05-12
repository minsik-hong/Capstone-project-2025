// frontend/src/components/SettingsModal.jsx
import React, { useState } from 'react';
import './SettingsModal.css';
import MemoryManagerModal from './MemoryManagerModal';
import { refreshUserProfile } from '../../services/api';

export default function SettingsModal({ trigger, currentEmail = "user@example.com" }) {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState("profile");
  const [newEmail, setNewEmail] = useState("");
  const [showManager, setShowManager] = useState(false);
  const [profileSummary, setProfileSummary] = useState(null);

  return (
    <>
      <span onClick={() => setOpen(true)}>{trigger}</span>

      {open && (
        <div className="modal-overlay" onClick={() => setOpen(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <nav className="modal-aside">
              <button className={tab === "profile" ? "tab-btn active" : "tab-btn"} onClick={() => setTab("profile")}>프로필</button>
              <button className={tab === "memory" ? "tab-btn active" : "tab-btn"} onClick={() => setTab("memory")}>메모리</button>
            </nav>

            <section className="modal-main">
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

                  {/* 사용자 성향 분석 버튼 */}
                  <div className="action-row" style={{ marginTop: "20px" }}>
                    <button
                      className="save-btn profile-analyze-btn"
                      onClick={async () => {
                        const userId = localStorage.getItem("user_id");
                        if (userId) {
                          try {
                            const result = await refreshUserProfile(userId);
                            setProfileSummary(result.profile);
                          } catch (err) {
                            alert("프로필 분석에 실패했습니다.");
                          }
                        } else {
                          alert("로그인된 사용자 정보가 없습니다.");
                        }
                      }}
                    >
                      🧠 영어 학습 성향 분석하기
                    </button>
                  </div>

                  {/* 분석 결과 표시 */}
                  {profileSummary && (
                    <div className="profile-summary-box">
                      <h4>📊 분석 요약 (Analysis Summary)</h4>
                      <p><strong>레벨(Level):</strong> {profileSummary.level}</p>
                      <p><strong>관심사(Interests):</strong> {profileSummary.interests.join(", ")}</p>
                      <p><strong>약점(Weaknesses):</strong> {profileSummary.weaknesses.join(", ")}</p>
                      <p><strong>요약(Summary):</strong> {profileSummary.summary}</p>
                    </div>
                  )}
                </div>
              )}

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

                  <div className="manage-link-row">
                    <button className="manage-memory-link" onClick={() => setShowManager(true)}>
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

                  {showManager && (
                    <MemoryManagerModal onClose={() => setShowManager(false)} />
                  )}
                </div>
              )}
            </section>

            <button className="close-btn" onClick={() => setOpen(false)}>×</button>
          </div>
        </div>
      )}
    </>
  );
}
