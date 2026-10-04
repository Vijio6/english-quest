import sqlite3

DB_NAME = "game.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Drop existing questions to rebuild with difficulty column
    cursor.execute("DROP TABLE IF EXISTS questions")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty TEXT NOT NULL,
            category TEXT NOT NULL,
            prompt TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            options TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            streak INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    seed_questions = [
        # --- BEGINNER ---
        ("beginner", "vocabulary", "What is the synonym of 'Happy'?", "Joyful", "Joyful,Gloomy,Angry,Tired", "'Joyful' means feeling or expressing great happiness."),
        ("beginner", "grammar", "She ___ to school every single morning.", "walks", "walk,walks,walking,walked", "Singular third-person subject ('She') requires the singular present verb 'walks'."),
        ("beginner", "vocabulary", "Choose the antonym of 'Difficult':", "Easy", "Hard,Easy,Complex,Strict", "'Easy' is the opposite of difficult."),
        ("beginner", "grammar", "They ___ watching a movie right now.", "are", "is,are,was,am", "Plural subject 'They' pairs with 'are' in the present continuous tense."),

        # --- INTERMEDIATE ---
        ("intermediate", "vocabulary", "Choose the closest synonym for 'Candid':", "Frank", "Deceptive,Frank,Secretive,Shy", "Candid means straightforward, honest, and frank."),
        ("intermediate", "grammar", "If she ___ earlier, she would have caught the bus.", "had left", "left,had left,would leave,has left", "Third conditional uses 'had + past participle' in the condition clause."),
        ("intermediate", "vocabulary", "Choose the antonym of 'Mitigate':", "Aggravate", "Aggravate,Alleviate,Subside,Soothe", "Mitigate means to lessen severity; aggravate means to make worse."),
        ("intermediate", "grammar", "Neither the teacher nor the students ___ in the lab.", "were", "was,were,is,are being", "In 'neither/nor' sentences, the verb agrees with the closest subject ('students')."),

        # --- VETERAN ---
        ("veteran", "vocabulary", "Choose the closest synonym for 'Sesquipedalian':", "Polysyllabic", "Laconic,Polysyllabic,Ephemeral,Puerile", "Sesquipedalian refers to long words or someone fond of using long words."),
        ("veteran", "grammar", "Seldom ___ such an intricate display of dialectical rhetoric.", "had he encountered", "he had encountered,had he encountered,he has encountered,did he encountered", "Negative adverb 'Seldom' at the sentence start triggers subject-auxiliary inversion."),
        ("veteran", "vocabulary", "Choose the antonym of 'Truculent':", "Placid", "Placid,Bellicose,Pugnacious,Acerbic", "Truculent means aggressive and defiant; placid means calm and peaceful."),
        ("veteran", "grammar", "I insist that the committee ___ the resolution without delay.", "review", "reviews,reviewed,review,will review", "The subjunctive mood following verbs of demand ('insist that') takes the base form.")
    ]

    cursor.executemany("""
        INSERT INTO questions (difficulty, category, prompt, correct_answer, options, explanation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, seed_questions)

    conn.commit()
    conn.close()
    print("Database re-initialized with Beginner, Intermediate, and Veteran questions!")

if __name__ == "__main__":
    init_db()