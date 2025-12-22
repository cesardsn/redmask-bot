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
        name TEXT UNIQUE,
        world TEXT,
        level INTEGER,
        voc TEXT,
        guild_name TEXT,
        last_update TEXT,
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
def add_or_update_character(telegram_id, char):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO characters
    (telegram_id, name, world, level, voc, guild_name, last_update)
    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
    ON CONFLICT(name) DO UPDATE SET
        telegram_id=excluded.telegram_id,
        world=excluded.world,
        level=excluded.level,
        voc=excluded.voc,
        guild_name=excluded.guild_name,
        last_update=datetime('now')
    """, (
        telegram_id,
        char["name"],
        char["world"],
        char["level"],
        char["voc"],
        char["guild"]
    ))

    conn.commit()
    conn.close()
