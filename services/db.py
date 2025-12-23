import sqlite3
from config import DB_FILE

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Usuários
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        char_name TEXT,
        premium INTEGER DEFAULT 0
    )
    """)
    
    # Limites diários
    c.execute("""
    CREATE TABLE IF NOT EXISTS limits (
        telegram_id INTEGER,
        feature TEXT,
        uses INTEGER DEFAULT 0,
        date TEXT,
        PRIMARY KEY (telegram_id, feature, date)
    )
    """)

    # Pagamentos manuais
    c.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        char_name TEXT,
        value INTEGER,
        confirmed INTEGER DEFAULT 0,
        date TEXT
    )
    """)

    # Patrocinadores
    c.execute("""
    CREATE TABLE IF NOT EXISTS sponsors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        char_name TEXT,
        value INTEGER,
        date TEXT
    )
    """)
    
    conn.commit()
    conn.close()

# Inicializa banco ao importar
init_db()
