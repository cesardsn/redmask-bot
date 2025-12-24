from services.db import get_connection
from datetime import date
from config import DAILY_LIMIT

def check_limit(telegram_id, feature):
    """
    Verifica se o usuário atingiu o limite diário de uso de uma função.
    Retorna True se pode usar, False se já atingiu o limite (para Free).
    Usuários Premium não têm limite.
    """
    today = date.today().isoformat()
    conn = get_connection()
    c = conn.cursor()
    
    # Verifica se é Premium
    c.execute("SELECT premium FROM users WHERE telegram_id = ?", (telegram_id,))
    user = c.fetchone()
    is_premium = user["premium"] if user else 0

    if is_premium:
        conn.close()
        return True

    # Verifica limite diário
    c.execute("SELECT uses FROM limits WHERE telegram_id = ? AND feature = ? AND date = ?",
              (telegram_id, feature, today))
    row = c.fetchone()

    if row:
        if row["uses"] >= DAILY_LIMIT:
            conn.close()
            return False
        else:
            c.execute("UPDATE limits SET uses = uses + 1 WHERE telegram_id = ? AND feature = ? AND date = ?",
                      (telegram_id, feature, today))
    else:
        c.execute("INSERT INTO limits (telegram_id, feature, uses, date) VALUES (?, ?, ?, ?)",
                  (telegram_id, feature, 1, today))
    
    conn.commit()
    conn.close()
    return True
