import sqlite3

DB_NAME = "redmask.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Usuários (Telegram)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        username TEXT
    )
    """)

    # Characters vinculados ao Telegram
    cur.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        name TEXT,
        FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
    )
    """)

    conn.commit()
    conn.close()


def add_user(telegram_id, username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users (telegram_id, username)
    VALUES (?, ?)
    """, (telegram_id, username))

    conn.commit()
    conn.close()


def add_character(telegram_id, char_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO characters (telegram_id, name)
    VALUES (?, ?)
    """, (telegram_id, char_name))

    conn.commit()
    conn.close()


def get_characters(telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT name FROM characters
    WHERE telegram_id = ?
    """, (telegram_id,))

    chars = [row[0] for row in cur.fetchall()]
    conn.close()
    return chars
