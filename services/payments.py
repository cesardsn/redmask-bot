from services.db import get_connection
from datetime import datetime

def create_payment(telegram_id, char_name, value):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO payments (telegram_id, char_name, value, date) VALUES (?, ?, ?, ?)",
              (telegram_id, char_name, value, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def confirm_payment(payment_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT telegram_id, char_name, value FROM payments WHERE id = ?", (payment_id,))
    row = c.fetchone()
    if row:
        # confirma pagamento
        c.execute("UPDATE payments SET confirmed = 1 WHERE id = ?", (payment_id,))
        # seta premium
        c.execute("UPDATE users SET premium = 1 WHERE telegram_id = ?", (row["telegram_id"],))
    conn.commit()
    conn.close()
