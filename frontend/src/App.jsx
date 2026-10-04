import React, { useState, useEffect, useRef } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000/api";

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
    summary: "Basic vocabulary, standard present & past verbs, everyday conversational English.",
    topics: ["Essential Synonyms", "Subject-Verb Agreement", "Simple Tenses"]
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
    summary: "Phrasal verbs, tricky idioms, conditionals, and nuance-driven context clues.",
    topics: ["Conditionals & Conjunctions", "Contextual Vocabulary", "Preposition Pairs"]
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
    summary: "Archaic & GRE-grade vocabulary, grammatical inversion, subjunctive mood, and dialectics.",
    topics: ["Rare Lexicon", "Subject-Auxiliary Inversion", "Subjunctive Mood"]
  }
};

// Built-in Synthesizer SFX
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
    // Audio Context disabled by browser policy
  }
};

export default function App() {
  // Navigation / Phase: "dashboard" | "select-difficulty" | "arena" | "gameover" | "leaderboard"
  const [screen, setScreen] = useState("dashboard");

  // Player state
  const [playerName] = useState("Viji");
  const [xp, setXp] = useState(180);
  const [highScore, setHighScore] = useState(0);

  // Active game session state
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

  // Global Leaderboard
  const [leaderboard, setLeaderboard] = useState([]);

  // Round Timer
  const [timeLeft, setTimeLeft] = useState(15);
  const timerRef = useRef(null);

  const level = Math.floor(xp / 100) + 1;
  const currentLevelProgress = xp % 100;

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  // Timer loop for arena questions
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
      explanation: "Timeout! In linguistic combat, decisiveness is key."
    });
  };

  const fetchLeaderboard = async () => {
    try {
      const res = await fetch(`${API_BASE}/leaderboard`);
      const data = await res.json();
      setLeaderboard(data);
    } catch (e) {
      console.error("Leaderboard fetch error:", e);
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
      console.error("Failed to load questions:", err);
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
      setXp((prev) => prev + 25 * cfg.multiplier);
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
      {/* GLOBAL TOP NAV */}
      <header className="main-nav">
        <div className="brand-lockup" onClick={() => { playSound("click"); setScreen("dashboard"); }}>
          <span className="logo-gem">⚔️</span>
          <div>
            <h1 className="logo-title">ENGLISH QUEST</h1>
            <span className="logo-sub">TACTICAL LINGUISTIC ARENA</span>
          </div>
        </div>

        <div className="nav-controls">
          <div className="player-summary">
            <span className="avatar-pill">👑</span>
            <div className="player-text">
              <span className="name">{playerName}</span>
              <span className="rank-tag">Lvl {level} Commander</span>
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

      {/* VIEW: MAIN DASHBOARD MENU */}
      {screen === "dashboard" && (
        <main className="dashboard-view">
          {/* Hero Banner */}
          <div className="hero-banner">
            <div className="hero-content">
              <span className="tag-hero">READY FOR COMBAT</span>
              <h2 className="hero-title">Forge Your Vocabulary & Rule The Grammar Protocol</h2>
              <p className="hero-desc">
                Sharpen syntax, master high-level vocabulary, and climb ranks. Pick between Beginner,
                Intermediate, or Veteran challenges to push your verbal precision.
              </p>
              <button 
                className="cta-primary-btn" 
                onClick={() => { playSound("click"); setScreen("select-difficulty"); }}
              >
                🎮 START QUEST
              </button>
            </div>

            <div className="hero-stats-card">
              <h3>COMMANDER PROFILE</h3>
              <div className="xp-metric">
                <div className="xp-text">
                  <span>PROGRESSION</span>
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
                  <span className="mini-label">ACTIVE LEVEL</span>
                  <span className="mini-val purple">LVL {level}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Rules / Overview Grid */}
          <div className="briefing-grid">
            <div className="briefing-card">
              <span className="card-icon">⚡</span>
              <h4>Dynamic AI Engine</h4>
              <p>Groq LLaMA-3 powers generated on-the-fly questions when you want unique verbal challenges.</p>
            </div>
            <div className="briefing-card">
              <span className="card-icon">🔥</span>
              <h4>Combat Streaks</h4>
              <p>Maintain consecutive correct answers to multiply point yields and advance your global standing.</p>
            </div>
            <div className="briefing-card">
              <span className="card-icon">⏱️</span>
              <h4>Countdown Pressure</h4>
              <p>Higher difficulty tiers cut your clock down to 10 seconds. Hesitation means failure.</p>
            </div>
          </div>
        </main>
      )}

      {/* VIEW: SELECT DIFFICULTY */}
      {screen === "select-difficulty" && (
        <main className="select-view">
          <div className="select-header">
            <span className="tag-hero">PROTOCOL STEP 1</span>
            <h2>Select Difficulty Tier</h2>
            <p>Pick the battlefield that matches your current command of the English language.</p>
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

                <button className="tier-start-btn">ENGAGE {tier.label.toUpperCase()} →</button>
              </div>
            ))}
          </div>

          <button 
            className="back-btn" 
            onClick={() => { playSound("click"); setScreen("dashboard"); }}
          >
            ← Return to Dashboard
          </button>
        </main>
      )}

      {/* VIEW: QUESTION ARENA */}
      {screen === "arena" && (
        <main className="arena-view">
          {loading ? (
            <div className="loading-box">
              <div className="pulse-spinner"></div>
              <p>Loading questions for {DIFFICULTY_CONFIG[chosenDifficulty]?.label} tier...</p>
            </div>
          ) : currentQ ? (
            <div className="arena-card">
              {/* Top Countdown Bar */}
              <div className="timer-track">
                <div 
                  className="timer-fill" 
                  style={{ 
                    width: `${timerPercentage}%`, 
                    background: timeLeft < 5 ? "var(--red)" : "var(--accent)" 
                  }}
                ></div>
              </div>

              {/* Arena HUD */}
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
                  <span className="hud-metric">Round {currentIndex + 1} / {questions.length}</span>
                  <span className="hud-metric">Score: <strong className="cyan">{sessionScore}</strong></span>
                  <span className="hud-metric">Streak: <strong className="orange">🔥 {streak}</strong></span>
                  <span className="hud-timer" style={{ color: timeLeft < 5 ? "var(--red)" : "var(--text)" }}>⏱️️ {timeLeft}s</span>
                </div>
              </div>

              <h2 className="arena-prompt">{currentQ.prompt}</h2>

              {/* Options Grid */}
              <div className="arena-options">
                {currentQ.options?.map((opt, idx) => {
                  let status = "";
                  if (selectedOption !== null) {
                    if (feedback?.is_correct && selectedOption === opt) status = "correct";
                    else if (!feedback?.is_correct && selectedOption === opt) status = "wrong";
                    else if (!feedback?.is_correct && opt.toLowerCase() === feedback?.correct_answer?.toLowerCase()) status = "reveal";
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

              {/* Feedback box */}
              {feedback && (
                <div className={`feedback-banner ${feedback.is_correct ? "correct" : "wrong"}`}>
                  <div className="feedback-title">
                    {feedback.is_correct ? "✓ EXCELLENT! POINT SECURED" : `✗ INCORRECT — ANSWER: ${feedback.correct_answer}`}
                  </div>
                  <p className="feedback-body">{feedback.explanation}</p>
                </div>
              )}

              {/* Bottom controls */}
              <div className="arena-controls">
                {selectedOption !== null && (
                  <button className="cta-primary-btn" onClick={handleNextQuestion}>
                    {currentIndex + 1 === questions.length ? "Finish Engagement" : "Next Question →"}
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
            <p>No questions returned for this difficulty.</p>
          )}
        </main>
      )}

      {/* VIEW: GAME OVER DEBRIEF */}
      {screen === "gameover" && (
        <main className="gameover-view">
          <div className="gameover-card">
            <span className="badge category-badge">PROTOCOL COMPLETED</span>
            <h2>Engagement Debrief</h2>
            <div className="final-score-display">
              <span className="big-score">{sessionScore}</span>
              <span className="score-unit">POINTS EARNED</span>
            </div>

            <div className="debrief-stats">
              <div className="debrief-stat">
                <span>Tier Selected</span>
                <strong style={{ color: DIFFICULTY_CONFIG[chosenDifficulty]?.color }}>
                  {DIFFICULTY_CONFIG[chosenDifficulty]?.label}
                </strong>
              </div>
              <div className="debrief-stat">
                <span>Max Streak</span>
                <strong className="orange">🔥 {maxSessionStreak}</strong>
              </div>
            </div>

            <div className="gameover-actions">
              <button 
                className="cta-primary-btn" 
                onClick={() => startGameWithDifficulty(chosenDifficulty)}
              >
                Replay {DIFFICULTY_CONFIG[chosenDifficulty]?.label}
              </button>
              <button 
                className="secondary-btn" 
                onClick={() => { playSound("click"); setScreen("select-difficulty"); }}
              >
                Change Difficulty
              </button>
              <button 
                className="secondary-btn" 
                onClick={() => { playSound("click"); setScreen("dashboard"); }}
              >
                Main Dashboard
              </button>
            </div>
          </div>
        </main>
      )}

      {/* VIEW: LEADERBOARD */}
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

            <button 
              className="back-btn" 
              onClick={() => { playSound("click"); setScreen("dashboard"); }}
            >
              ← Back to Dashboard
            </button>
          </div>
        </main>
      )}
    </div>
  );
}