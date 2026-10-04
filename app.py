import os
import json
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
from database import init_db, get_connection

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure database is primed on startup
init_db()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

@app.route("/api/questions", methods=["GET"])
def get_questions():
    difficulty = request.args.get("difficulty", "beginner").lower().strip()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Randomly select 5 questions from the 100 questions for this difficulty
    cursor.execute(
        "SELECT id, difficulty, category, prompt, options, explanation FROM questions WHERE LOWER(difficulty) = ? ORDER BY RANDOM() LIMIT 5",
        (difficulty,)
    )
    rows = cursor.fetchall()

    # Fallback if DB was clean
    if not rows or len(rows) < 5:
        init_db()
        cursor.execute(
            "SELECT id, difficulty, category, prompt, options, explanation FROM questions WHERE LOWER(difficulty) = ? ORDER BY RANDOM() LIMIT 5",
            (difficulty,)
        )
        rows = cursor.fetchall()

    conn.close()

    payload = [
        {
            "id": row["id"],
            "difficulty": row["difficulty"],
            "category": row["category"],
            "prompt": row["prompt"],
            "options": row["options"].split(","),
            "explanation": row["explanation"]
        }
        for row in rows
    ]
    return jsonify(payload)

@app.route("/api/verify", methods=["POST"])
def verify_answer():
    data = request.get_json() or {}
    question_id = data.get("question_id")
    user_answer = data.get("answer", "").strip().lower()

    if not question_id:
        return jsonify({"error": "Missing question_id"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT correct_answer, explanation FROM questions WHERE id = ?", (question_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Question not found"}), 404

    correct_answer = row["correct_answer"]
    is_correct = user_answer == correct_answer.strip().lower()

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": row["explanation"]
    })

@app.route("/api/generate-question", methods=["GET"])
def generate_ai_question():
    if not groq_client:
        return jsonify({"error": "Groq API key not configured"}), 500

    difficulty = request.args.get("difficulty", "beginner").lower()
    
    tier_guides = {
        "beginner": "Focus on everyday vocabulary, simple anagrams, basic idioms, or synonyms/antonyms.",
        "intermediate": "Focus on idioms, multi-letter anagrams, phrasal subtleties, or collegiate vocabulary.",
        "veteran": "Focus on archaic, GRE/SAT grade lexicon, obscure anagrams, ancient etymological idioms, or subjunctive structures."
    }
    guide = tier_guides.get(difficulty, tier_guides["beginner"])

    prompt = f"""
    Create one four-option multiple-choice English question.
    Difficulty: {difficulty.upper()}.
    Guideline: {guide}
    Categories can be: synonym, antonym, anagram, idiom, or vocabulary.
    Return strictly JSON:
    {{
      "category": "idiom",
      "difficulty": "{difficulty}",
      "prompt": "Question text here",
      "options": ["Choice A", "Choice B", "Choice C", "Choice D"],
      "correct_answer": "Choice A",
      "explanation": "Why this answer is correct"
    }}
    """

    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a master English linguist and quiz architect. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)
        data["id"] = 999999
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/score", methods=["POST"])
def save_score():
    data = request.get_json() or {}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scores (player_name, difficulty, score, streak) VALUES (?, ?, ?, ?)",
        (data.get("player_name", "Explorer"), data.get("difficulty", "beginner"), data.get("score", 0), data.get("streak", 0))
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT player_name, difficulty, score, streak, created_at 
        FROM scores 
        ORDER BY score DESC 
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)