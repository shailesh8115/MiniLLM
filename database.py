import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================================================
# DATABASE CONFIG
# ==========================================================

DB_DIR = Path("database")
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "minillm.db"


# ==========================================================
# CONNECTION
# ==========================================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# CREATE TABLES
# ==========================================================

def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    # ---------------- USERS ----------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- CHAT ----------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        question TEXT,

        answer TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- RESUME ----------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS resumes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        filename TEXT,

        content TEXT,

        ats_score INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- SEARCH ----------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS search_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        query TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- OCR ----------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ocr_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        filename TEXT,

        extracted_text TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# REGISTER USER
# ==========================================================

def register_user(username, email, password):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO users
            (username,email,password)

            VALUES(?,?,?)
            """,
            (
                username,
                email,
                generate_password_hash(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ==========================================================
# LOGIN
# ==========================================================

def login(username, password):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    if row is None:

        return False

    return check_password_hash(
        row["password"],
        password
    )


# ==========================================================
# GET USER
# ==========================================================

def get_user(username):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cur.fetchone()

    conn.close()

    return user
# ==========================================================
# CHAT HISTORY
# ==========================================================

def save_chat(username, question, answer):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chat_history
        (username, question, answer)
        VALUES (?, ?, ?)
        """,
        (username, question, answer)
    )

    conn.commit()
    conn.close()


def load_chat(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT question, answer
        FROM chat_history
        WHERE username=?
        ORDER BY id ASC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return [
        (row["question"], row["answer"])
        for row in rows
    ]


def clear_chat(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM chat_history
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# RESUME
# ==========================================================

def save_resume(
    username,
    filename,
    content,
    ats_score=0
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO resumes
        (username, filename, content, ats_score)

        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            filename,
            content,
            ats_score
        )
    )

    conn.commit()
    conn.close()


def load_resumes(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM resumes

        WHERE username=?

        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def delete_resume(resume_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM resumes
        WHERE id=?
        """,
        (resume_id,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# SEARCH HISTORY
# ==========================================================

def save_search(username, query):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO search_history
        (username, query)

        VALUES (?, ?)
        """,
        (
            username,
            query
        )
    )

    conn.commit()
    conn.close()


def load_search_history(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *

        FROM search_history

        WHERE username=?

        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================================================
# OCR HISTORY
# ==========================================================

def save_ocr(username, filename, extracted_text):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ocr_history
        (username, filename, extracted_text)

        VALUES (?, ?, ?)
        """,
        (
            username,
            filename,
            extracted_text
        )
    )

    conn.commit()
    conn.close()


def load_ocr_history(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *

        FROM ocr_history

        WHERE username=?

        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows
# ==========================================================
# DASHBOARD STATS
# ==========================================================

def dashboard_stats(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM chat_history WHERE username=?",
        (username,)
    )
    chats = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM resumes WHERE username=?",
        (username,)
    )
    resumes = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM search_history WHERE username=?",
        (username,)
    )
    searches = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM ocr_history WHERE username=?",
        (username,)
    )
    ocr = cur.fetchone()[0]

    conn.close()

    return {
        "chats": chats,
        "resumes": resumes,
        "searches": searches,
        "ocr": ocr
    }


# ==========================================================
# COUNT FUNCTIONS
# ==========================================================

def count_chat(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM chat_history WHERE username=?",
        (username,)
    )

    total = cur.fetchone()[0]

    conn.close()

    return total


def count_resume(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM resumes WHERE username=?",
        (username,)
    )

    total = cur.fetchone()[0]

    conn.close()

    return total


def count_search(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM search_history WHERE username=?",
        (username,)
    )

    total = cur.fetchone()[0]

    conn.close()

    return total


def count_ocr(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM ocr_history WHERE username=?",
        (username,)
    )

    total = cur.fetchone()[0]

    conn.close()

    return total


# ==========================================================
# RECENT ACTIVITY
# ==========================================================

def recent_chat(username, limit=5):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT question, answer
        FROM chat_history
        WHERE username=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (username, limit)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================================================
# UPDATE PROFILE
# ==========================================================

def update_user(username, email):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET email=?
        WHERE username=?
        """,
        (
            email,
            username
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

def change_password(username, new_password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            generate_password_hash(new_password),
            username
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# DELETE ACCOUNT
# ==========================================================

def delete_user(username):

    conn = get_connection()
    cur = conn.cursor()

    # Delete related records first

    cur.execute(
        "DELETE FROM chat_history WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM resumes WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM search_history WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM ocr_history WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# RESET USER DATA
# ==========================================================

def reset_user(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM chat_history WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM resumes WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM search_history WHERE username=?",
        (username,)
    )

    cur.execute(
        "DELETE FROM ocr_history WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

create_tables()