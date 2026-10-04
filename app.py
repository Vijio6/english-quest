import os
import json
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DB_NAME = "game.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

@app.route("/api/questions", methods=["GET"])
def get_questions():
    difficulty = request.args.get("difficulty", "beginner").lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, difficulty, category, prompt, options, explanation FROM questions WHERE difficulty = ? ORDER BY RANDOM()",
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
    is_correct = user_answer == correct_answer.lower()

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
        "beginner": "Focus on everyday A2/B1 vocabulary and basic present/past tense grammar.",
        "intermediate": "Focus on B2/C1 vocabulary, phrasal verbs, idioms, and conditional grammar.",
        "veteran": "Focus on GRE/SAT level C2 vocabulary, arcane words, inversion, and subjunctive grammar."
    }
    guide = tier_guides.get(difficulty, tier_guides["beginner"])

    prompt = f"""
    Create one multiple-choice English question.
    Difficulty Tier: {difficulty.upper()}.
    Guideline: {guide}
    Output ONLY a JSON object matching this exact schema:
    {{
      "category": "vocabulary",
      "difficulty": "{difficulty}",
      "prompt": "The question sentence",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why this option is correct"
    }}
    """

    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional English linguist. Output only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)
        data["id"] = 999999  # Temporary ID for dynamically generated questions
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
        LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)