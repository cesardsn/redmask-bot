from services.db import get_connection
from datetime import date
from config import DAILY_LIMIT

def check_limit(telegram_id, feature):
    today = date.today().isoformat()
    conn = get_connection()
    c = conn.cursor()
    
    # Verifica limite atual
    c.execute("SELECT uses FROM limits WHERE telegram_id = ? AND feature = ? AND date = ?", (telegram_id, feature, today))
    row = c.fetchone()
    
    # Verifica se é premium
    c.execute("SELECT premium FROM users WHERE telegram_id = ?", (telegram_id,))
    user = c.fetchone()
    is_premium = user["premium"] if user else 0
    
    if not is_premium:
        if row and row["uses"] >= DAILY_LIMIT:
            conn.close()
            return False
        elif row:
            c.execute("UPDATE limits SET uses = uses + 1 WHERE telegram_id = ? AND feature = ? AND date = ?", (telegram_id, feature, today))
        else:
            c.execute("INSERT INTO limits (telegram_id, feature, uses, date) VALUES (?, ?, 1, ?)", (telegram_id, feature, today))
        conn.commit()
    
    conn.close()
    return True
