from services.db import get_connection
from datetime import date

def create_payment(telegram_id, char_name, value):
    """
    Cria um registro de pagamento manual
    """
    conn = get_connection()
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("""
        INSERT INTO payments (telegram_id, char_name, value, confirmed, date)
        VALUES (?, ?, ?, 0, ?)
    """, (telegram_id, char_name, value, today))
    conn.commit()
    conn.close()
    return True

def confirm_payment(payment_id):
    """
    Marca pagamento como confirmado
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE payments SET confirmed = 1 WHERE id = ?", (payment_id,))
    conn.commit()
    conn.close()

def list_pending_payments():
    """
    Retorna lista de pagamentos pendentes
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM payments WHERE confirmed = 0 ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def list_confirmed_payments():
    """
    Retorna lista de pagamentos confirmados
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM payments WHERE confirmed = 1 ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_sponsors(top=3):
    """
    Retorna os top 3 patrocinadores do dia
    """
    today = date.today().isoformat()
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT char_name, value FROM payments
        WHERE confirmed = 1 AND date = ?
        ORDER BY value DESC LIMIT ?
    """, (today, top))
    rows = c.fetchall()
    conn.close()
    return rows
