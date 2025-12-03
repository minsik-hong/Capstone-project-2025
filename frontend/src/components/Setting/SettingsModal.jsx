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
                    <div className="profile-summary-card">
                      <div className="summary-header">
                        <span className="summary-icon">📊</span>
                        <h4>학습 성향 분석 결과</h4>
                      </div>
                      
                      <div className="summary-grid">
                        <div className="summary-item level-item">
                          <div className="item-label">🎯 영어 레벨</div>
                          <div className="item-value level-badge">{profileSummary.level}</div>
                          <div className="item-desc">
                            {profileSummary.level === 'A1' && '입문 단계 - 기초적인 표현을 이해하고 사용할 수 있어요'}
                            {profileSummary.level === 'A2' && '초급 단계 - 간단한 일상 대화가 가능해요'}
                            {profileSummary.level === 'B1' && '중급 단계 - 일상적인 주제에 대해 대화할 수 있어요'}
                            {profileSummary.level === 'B2' && '중상급 단계 - 복잡한 주제도 다룰 수 있어요'}
                            {profileSummary.level === 'C1' && '고급 단계 - 유창하게 의사소통할 수 있어요'}
                            {profileSummary.level === 'C2' && '원어민 수준 - 거의 모든 상황에서 완벽하게 소통해요'}
                          </div>
                        </div>

                        <div className="summary-item">
                          <div className="item-label">💡 관심 분야</div>
                          <div className="item-tags">
                            {profileSummary.interests.map((interest, i) => (
                              <span key={i} className="tag interest-tag">{interest}</span>
                            ))}
                          </div>
                          <div className="item-desc">이 주제들로 학습하면 더 효과적이에요!</div>
                        </div>

                        <div className="summary-item">
                          <div className="item-label">📝 보완이 필요한 부분</div>
                          <div className="item-tags">
                            {profileSummary.weaknesses.map((weakness, i) => (
                              <span key={i} className="tag weakness-tag">{weakness}</span>
                            ))}
                          </div>
                          <div className="item-desc">이 부분을 집중적으로 연습해보세요!</div>
                        </div>
                      </div>

                      <div className="summary-detail">
                        <div className="detail-label">🔍 상세 분석</div>
                        <div className="detail-bilingual">
                          <p className="detail-text-en">{profileSummary.summary}</p>
                          {profileSummary.summary_ko && (
                            <p className="detail-text-ko">{profileSummary.summary_ko}</p>
                          )}
                        </div>
                      </div>
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
