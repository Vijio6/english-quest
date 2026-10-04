import React, { useState, useEffect, useRef } from "react";
import "./App.css";

const API_BASE = "https://english-quest-g2mj.onrender.com/api";

const DIFFICULTY_CONFIG = {
  beginner: {
    id: "beginner",
    label: "Beginner",
    subtitle: "A2 - B1 Foundation",
    badge: "🟢 Tier I",
    color: "#10b981",
    multiplier: 1,
    basePoints: 10,
    time: 20,
    summary: "100 curated questions: everyday vocabulary, basic idioms, easy anagrams & core synonyms.",
    topics: ["Essential Synonyms & Antonyms", "4-Letter Anagrams", "Popular Idioms"]
  },
  intermediate: {
    id: "intermediate",
    label: "Intermediate",
    subtitle: "B2 Working Fluency",
    badge: "🔵 Tier II",
    color: "#38bdf8",
    multiplier: 2,
    basePoints: 20,
    time: 15,
    summary: "100 curated questions: nuanced vocabulary, multi-word anagrams, phrasal idioms & context clues.",
    topics: ["Contextual Synonyms", "Clever Anagrams", "Nuanced Idioms & Phrases"]
  },
  veteran: {
    id: "veteran",
    label: "Veteran",
    subtitle: "C1 - C2 Mastery / GRE",
    badge: "🟣 Tier III",
    color: "#ec4899",
    multiplier: 3,
    basePoints: 35,
    time: 10,
    summary: "100 curated questions: arcane lexicon, classical anagrams, historical idioms & academic syntax.",
    topics: ["GRE Lexicon", "Complex Anagrams", "Etymological & Historical Idioms"]
  }
};

const playSound = (type) => {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    if (type === "correct") {
      osc.type = "sine";
      osc.frequency.setValueAtTime(523.25, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(783.99, ctx.currentTime + 0.15);
      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    } else if (type === "wrong") {
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(160, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(90, ctx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.25, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
      osc.start();
      osc.stop(ctx.currentTime + 0.25);
    } else if (type === "click") {
      osc.type = "triangle";
      osc.frequency.setValueAtTime(440, ctx.currentTime);
      gain.gain.setValueAtTime(0.06, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    }
  } catch (e) {
    // Audio Context disabled
  }
};

export default function App() {
  const [screen, setScreen] = useState("dashboard"); // dashboard | select-difficulty | arena | gameover | leaderboard

  // Editable username stored in localStorage
  const [playerName, setPlayerName] = useState(() => {
    return localStorage.getItem("english_quest_username") || "Player " + Math.floor(100 + Math.random() * 900);
  });
  const [isEditingName, setIsEditingName] = useState(false);
  const [nameInput, setNameInput] = useState(playerName);

  const [xp, setXp] = useState(120);
  const [highScore, setHighScore] = useState(0);

  const [chosenDifficulty, setChosenDifficulty] = useState("beginner");
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [sessionScore, setSessionScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [maxSessionStreak, setMaxSessionStreak] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiGenerating, setAiGenerating] = useState(false);
  const [leaderboard, setLeaderboard] = useState([]);
  const [timeLeft, setTimeLeft] = useState(15);
  const timerRef = useRef(null);

  const level = Math.floor(xp / 100) + 1;
  const currentLevelProgress = xp % 100;

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const saveCustomUsername = () => {
    const trimmed = nameInput.trim();
    if (trimmed) {
      setPlayerName(trimmed);
      localStorage.setItem("english_quest_username", trimmed);
    }
    setIsEditingName(false);
  };

  useEffect(() => {
    if (screen !== "arena" || selectedOption !== null || loading || questions.length === 0) {
      clearInterval(timerRef.current);
      return;
    }

    const tierLimit = DIFFICULTY_CONFIG[chosenDifficulty]?.time || 15;
    setTimeLeft(tierLimit);
    clearInterval(timerRef.current);

    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          handleTimeExpire();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timerRef.current);
  }, [currentIndex, screen, selectedOption, loading, questions]);

  const handleTimeExpire = () => {
    playSound("wrong");
    setSelectedOption("__EXPIRED__");
    setStreak(0);
    const activeQ = questions[currentIndex];
    setFeedback({
      is_correct: false,
      correct_answer: activeQ.correct_answer || "Time Expired",
      explanation: "Timeout! Swift decision-making is necessary under combat conditions."
    });
  };

  const fetchLeaderboard = async () => {
    try {
      const res = await fetch(`${API_BASE}/leaderboard`);
      const data = await res.json();
      setLeaderboard(data);
    } catch (e) {
      console.error(e);
    }
  };

  const startGameWithDifficulty = async (tier) => {
    playSound("click");
    setChosenDifficulty(tier);
    setLoading(true);
    setScreen("arena");

    try {
      const res = await fetch(`${API_BASE}/questions?difficulty=${tier}`);
      const data = await res.json();
      setQuestions(data);
      setCurrentIndex(0);
      setSessionScore(0);
      setStreak(0);
      setMaxSessionStreak(0);
      setSelectedOption(null);
      setFeedback(null);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = async (option) => {
    if (selectedOption !== null) return;
    clearInterval(timerRef.current);
    setSelectedOption(option);

    const activeQ = questions[currentIndex];
    let isCorrect = false;
    let explanation = "";

    if (activeQ.id === 999999) {
      isCorrect = option.trim().toLowerCase() === activeQ.correct_answer.trim().toLowerCase();
      explanation = activeQ.explanation;
      setFeedback({ is_correct: isCorrect, correct_answer: activeQ.correct_answer, explanation });
    } else {
      try {
        const res = await fetch(`${API_BASE}/verify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question_id: activeQ.id, answer: option })
        });
        const result = await res.json();
        isCorrect = result.is_correct;
        explanation = result.explanation;
        setFeedback(result);
      } catch (err) {
        console.error(err);
      }
    }

    const cfg = DIFFICULTY_CONFIG[chosenDifficulty];
    if (isCorrect) {
      playSound("correct");
      const earned = cfg.basePoints * cfg.multiplier + streak * 5;
      setSessionScore((prev) => prev + earned);
      setXp((prev) => prev + 20 * cfg.multiplier);
      const nextStreak = streak + 1;
      setStreak(nextStreak);
      if (nextStreak > maxSessionStreak) setMaxSessionStreak(nextStreak);
    } else {
      playSound("wrong");
      setStreak(0);
    }
  };

  const handleNextQuestion = () => {
    playSound("click");
    setSelectedOption(null);
    setFeedback(null);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      finishGame();
    }
  };

  const generateGroqQuestion = async () => {
    playSound("click");
    try {
      setAiGenerating(true);
      const res = await fetch(`${API_BASE}/generate-question?difficulty=${chosenDifficulty}`);
      const aiQ = await res.json();
      setQuestions([aiQ]);
      setCurrentIndex(0);
      setSelectedOption(null);
      setFeedback(null);
    } catch (err) {
      console.error(err);
    } finally {
      setAiGenerating(false);
    }
  };

  const finishGame = async () => {
    setScreen("gameover");
    if (sessionScore > highScore) setHighScore(sessionScore);

    try {
      await fetch(`${API_BASE}/score`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player_name: playerName,
          difficulty: chosenDifficulty,
          score: sessionScore,
          streak: maxSessionStreak
        })
      });
      fetchLeaderboard();
    } catch (err) {
      console.error(err);
    }
  };

  const currentQ = questions[currentIndex];
  const maxTimer = DIFFICULTY_CONFIG[chosenDifficulty]?.time || 15;
  const timerPercentage = (timeLeft / maxTimer) * 100;

  return (
    <div className="app-shell">
      {/* GLOBAL NAVBAR */}
      <header className="main-nav">
        <div className="brand-lockup" onClick={() => { playSound("click"); setScreen("dashboard"); }}>
          <span className="logo-gem">⚔️</span>
          <div>
            <h1 className="logo-title">ENGLISH QUEST</h1>
            <span className="logo-sub">100-QUESTION TACTICAL ARENA</span>
          </div>
        </div>

        <div className="nav-controls">
          {/* USERNAME EDITABLE BADGE */}
          <div className="player-summary">
            <span className="avatar-pill">👤</span>
            <div className="player-text">
              {isEditingName ? (
                <div className="username-edit-box">
                  <input
                    type="text"
                    className="username-input"
                    value={nameInput}
                    onChange={(e) => setNameInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && saveCustomUsername()}
                    autoFocus
                  />
                  <button className="save-username-btn" onClick={saveCustomUsername}>✓</button>
                </div>
              ) : (
                <span className="name" onClick={() => { setNameInput(playerName); setIsEditingName(true); }}>
                  {playerName} <small className="edit-icon">✏️</small>
                </span>
              )}
              <span className="rank-tag">Lvl {level} Inquisitor</span>
            </div>
          </div>

          <button 
            className={`nav-btn ${screen === "dashboard" ? "active" : ""}`}
            onClick={() => { playSound("click"); setScreen("dashboard"); }}
          >
            Dashboard
          </button>
          <button 
            className={`nav-btn ${screen === "leaderboard" ? "active" : ""}`}
            onClick={() => { playSound("click"); setScreen("leaderboard"); }}
          >
            Leaderboard
          </button>
        </div>
      </header>

      {/* DASHBOARD VIEW */}
      {screen === "dashboard" && (
        <main className="dashboard-view">
          <div className="hero-banner">
            <div className="hero-content">
              <span className="tag-hero">BATTLE ENGINE READY</span>
              <h2 className="hero-title">Forge Your Verbal Might Across 300 Curated Challenges</h2>
              <p className="hero-desc">
                Engage in rapid <strong>5-question tactical rounds</strong> drawn randomly from 100 dedicated
                questions per tier. Master Synonyms, Antonyms, Anagrams, Idioms, and Advanced Vocabulary.
              </p>
              <button 
                className="cta-primary-btn" 
                onClick={() => { playSound("click"); setScreen("select-difficulty"); }}
              >
                🎮 START QUEST
              </button>
            </div>

            <div className="hero-stats-card">
              <h3>COMMANDER DOSSIER</h3>
              <div className="xp-metric">
                <div className="xp-text">
                  <span>EXPERIENCE</span>
                  <span>{currentLevelProgress} / 100 XP</span>
                </div>
                <div className="xp-bar">
                  <div className="xp-fill" style={{ width: `${currentLevelProgress}%` }}></div>
                </div>
              </div>

              <div className="mini-stats-grid">
                <div className="mini-stat">
                  <span className="mini-label">ALL-TIME BEST</span>
                  <span className="mini-val cyan">{highScore} PTS</span>
                </div>
                <div className="mini-stat">
                  <span className="mini-label">PLAYER LEVEL</span>
                  <span className="mini-val purple">LVL {level}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="briefing-grid">
            <div className="briefing-card">
              <span className="card-icon">🔀</span>
              <h4>5 Random Questions</h4>
              <p>Each playthrough dynamically draws 5 fresh questions from the selected 100-question tier pool.</p>
            </div>
            <div className="briefing-card">
              <span className="card-icon">🧠</span>
              <h4>5 Core Disciplines</h4>
              <p>Vocabulary, Synonyms, Antonyms, Unscramble Anagrams, and High-Yield Idioms.</p>
            </div>
            <div className="briefing-card">
              <span className="card-icon">⚡</span>
              <h4>Infinite Groq AI</h4>
              <p>Generate endless novel challenges on-demand with LLaMA 3.3 70B AI integration.</p>
            </div>
          </div>
        </main>
      )}

      {/* SELECT DIFFICULTY VIEW */}
      {screen === "select-difficulty" && (
        <main className="select-view">
          <div className="select-header">
            <span className="tag-hero">PROTOCOL STEP 1</span>
            <h2>Choose Your Difficulty</h2>
            <p>100 questions per difficulty tier. 5 random questions selected each round.</p>
          </div>

          <div className="tier-cards-grid">
            {Object.values(DIFFICULTY_CONFIG).map((tier) => (
              <div 
                key={tier.id} 
                className="tier-card" 
                style={{ "--tier-accent": tier.color }}
                onClick={() => startGameWithDifficulty(tier.id)}
              >
                <div className="tier-card-badge">{tier.badge}</div>
                <h3 className="tier-card-title">{tier.label}</h3>
                <span className="tier-card-subtitle">{tier.subtitle}</span>
                <p className="tier-card-summary">{tier.summary}</p>

                <div className="tier-specs">
                  <div className="spec-row">
                    <span>Pool Size</span>
                    <strong>100 Questions</strong>
                  </div>
                  <div className="spec-row">
                    <span>Round Format</span>
                    <strong>5 Random Qs</strong>
                  </div>
                  <div className="spec-row">
                    <span>Score Multiplier</span>
                    <strong>{tier.multiplier}x Yield</strong>
                  </div>
                  <div className="spec-row">
                    <span>Turn Timer</span>
                    <strong>{tier.time}s per round</strong>
                  </div>
                </div>

                <div className="tier-topics">
                  {tier.topics.map((t, idx) => (
                    <span key={idx} className="topic-pill">{t}</span>
                  ))}
                </div>

                <button className="tier-start-btn">DEPLOY TO {tier.label.toUpperCase()} →</button>
              </div>
            ))}
          </div>

          <button className="back-btn" onClick={() => { playSound("click"); setScreen("dashboard"); }}>
            ← Return to Dashboard
          </button>
        </main>
      )}

      {/* ARENA VIEW */}
      {screen === "arena" && (
        <main className="arena-view">
          {loading ? (
            <div className="loading-box">
              <div className="pulse-spinner"></div>
              <p>Deploying 5 random {DIFFICULTY_CONFIG[chosenDifficulty]?.label} questions from 100-pool...</p>
            </div>
          ) : currentQ ? (
            <div className="arena-card">
              <div className="timer-track">
                <div 
                  className="timer-fill" 
                  style={{ 
                    width: `${timerPercentage}%`, 
                    background: timeLeft < 5 ? "var(--red)" : "var(--accent)" 
                  }}
                ></div>
              </div>

              <div className="arena-hud">
                <div className="hud-left">
                  <span className="badge category-badge">{currentQ.category?.toUpperCase()}</span>
                  <span 
                    className="badge tier-badge" 
                    style={{ borderColor: DIFFICULTY_CONFIG[chosenDifficulty]?.color, color: DIFFICULTY_CONFIG[chosenDifficulty]?.color }}
                  >
                    {DIFFICULTY_CONFIG[chosenDifficulty]?.label}
                  </span>
                </div>
                <div className="hud-right">
                  <span className="hud-metric">Question {currentIndex + 1} / {questions.length}</span>
                  <span className="hud-metric">Score: <strong className="cyan">{sessionScore}</strong></span>
                  <span className="hud-metric">Streak: <strong className="orange">🔥 {streak}</strong></span>
                  <span className="hud-timer" style={{ color: timeLeft < 5 ? "var(--red)" : "var(--text)" }}>⏱ {timeLeft}s</span>
                </div>
              </div>

              <h2 className="arena-prompt">{currentQ.prompt}</h2>

              <div className="arena-options">
                {currentQ.options?.map((opt, idx) => {
                  let status = "";
                  if (selectedOption !== null) {
                    if (feedback?.is_correct && selectedOption === opt) status = "correct";
                    else if (!feedback?.is_correct && selectedOption === opt) status = "wrong";
                    else if (!feedback?.is_correct && opt.trim().toLowerCase() === feedback?.correct_answer?.trim().toLowerCase()) status = "reveal";
                  }

                  return (
                    <button
                      key={idx}
                      className={`arena-opt-btn ${status}`}
                      disabled={selectedOption !== null}
                      onClick={() => handleSelectOption(opt)}
                    >
                      <span className="opt-marker">{["A", "B", "C", "D"][idx]}</span>
                      <span className="opt-text">{opt}</span>
                    </button>
                  );
                })}
              </div>

              {feedback && (
                <div className={`feedback-banner ${feedback.is_correct ? "correct" : "wrong"}`}>
                  <div className="feedback-title">
                    {feedback.is_correct ? "✓ CORRECT! POINT SECURED" : `✗ INCORRECT — ANSWER: ${feedback.correct_answer}`}
                  </div>
                  <p className="feedback-body">{feedback.explanation}</p>
                </div>
              )}

              <div className="arena-controls">
                {selectedOption !== null && (
                  <button className="cta-primary-btn" onClick={handleNextQuestion}>
                    {currentIndex + 1 === questions.length ? "View Protocol Results" : "Next Question →"}
                  </button>
                )}

                <button 
                  className="ai-forge-btn"
                  disabled={aiGenerating}
                  onClick={generateGroqQuestion}
                >
                  {aiGenerating ? "⚡ Synthesizing with Groq..." : "⚡ Forge Dynamic Groq AI Question"}
                </button>
              </div>
            </div>
          ) : (
            <p>No questions returned.</p>
          )}
        </main>
      )}

      {/* GAMEOVER DEBRIEF */}
      {screen === "gameover" && (
        <main className="gameover-view">
          <div className="gameover-card">
            <span className="badge category-badge">ROUND CONCLUDED</span>
            <h2>Tactical Debrief</h2>
            <div className="final-score-display">
              <span className="big-score">{sessionScore}</span>
              <span className="score-unit">POINTS EARNED</span>
            </div>

            <div className="debrief-stats">
              <div className="debrief-stat">
                <span>Operative</span>
                <strong>{playerName}</strong>
              </div>
              <div className="debrief-stat">
                <span>Difficulty</span>
                <strong style={{ color: DIFFICULTY_CONFIG[chosenDifficulty]?.color }}>
                  {DIFFICULTY_CONFIG[chosenDifficulty]?.label}
                </strong>
              </div>
              <div className="debrief-stat">
                <span>Peak Streak</span>
                <strong className="orange">🔥 {maxSessionStreak}</strong>
              </div>
            </div>

            <div className="gameover-actions">
              <button className="cta-primary-btn" onClick={() => startGameWithDifficulty(chosenDifficulty)}>
                Play Next 5 Questions ({DIFFICULTY_CONFIG[chosenDifficulty]?.label})
              </button>
              <button className="secondary-btn" onClick={() => { playSound("click"); setScreen("select-difficulty"); }}>
                Change Difficulty
              </button>
              <button className="secondary-btn" onClick={() => { playSound("click"); setScreen("dashboard"); }}>
                Return to Dashboard
              </button>
            </div>
          </div>
        </main>
      )}

      {/* LEADERBOARD VIEW */}
      {screen === "leaderboard" && (
        <main className="leaderboard-view">
          <div className="leaderboard-container">
            <div className="select-header">
              <h2>Global Operative Leaderboard</h2>
              <p>Top scores recorded across all difficulty engagements.</p>
            </div>

            <table className="leaderboard-tbl">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Operative</th>
                  <th>Difficulty</th>
                  <th>Max Streak</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((row, i) => (
                  <tr key={i}>
                    <td>#{i + 1}</td>
                    <td><strong>{row.player_name}</strong></td>
                    <td style={{ textTransform: "capitalize" }}>{row.difficulty}</td>
                    <td>🔥 {row.streak}</td>
                    <td className="cyan"><strong>{row.score}</strong></td>
                  </tr>
                ))}
              </tbody>
            </table>

            <button className="back-btn" onClick={() => { playSound("click"); setScreen("dashboard"); }}>
              ← Back to Dashboard
            </button>
          </div>
        </main>
      )}
    </div>
  );
}