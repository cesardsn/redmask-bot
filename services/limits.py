from services.db import get_connection

def register_user(telegram_id, char_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (telegram_id, char_name) VALUES (?, ?)", (telegram_id, char_name))
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    row = c.fetchone()
    conn.close()
    return row

def set_premium(telegram_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET premium = 1 WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()

def change_char(telegram_id, new_char):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET char_name = ? WHERE telegram_id = ?", (new_char, telegram_id))
    conn.commit()
    conn.close()
