import sqlite3
from datetime import datetime

DB_NAME = "database.db"


# ==============================
# CONEXÃO
# ==============================
def get_connection():
    return sqlite3.connect(DB_NAME)


# ==============================
# CRIAR TABELA DE DUELOS
# ==============================
def create_duel_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_telegram_id INTEGER NOT NULL,
            creator_char TEXT NOT NULL,
            world TEXT NOT NULL,
            min_level INTEGER NOT NULL,
            max_level INTEGER NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==============================
# CRIAR DUELO
# ==============================
def create_duel(
    telegram_id: int,
    creator_char: str,
    world: str,
    min_level: int,
    max_level: int
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO duels (
            creator_telegram_id,
            creator_char,
            world,
            min_level,
            max_level,
            status,
            created_at
        ) VALUES (?, ?, ?, ?, ?, 'open', ?)
    """, (
        telegram_id,
        creator_char,
        world,
        min_level,
        max_level,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ==============================
# VERIFICAR DUELO ATIVO DO USUÁRIO
# (ESSA FUNÇÃO ESTAVA FALTANDO ❌)
# ==============================
def get_user_active_duel(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM duels
        WHERE creator_telegram_id = ?
        AND status = 'open'
        LIMIT 1
    """, (telegram_id,))

    duel = cursor.fetchone()
    conn.close()

    return duel


# ==============================
# LISTAR DUELOS ABERTOS
# ==============================
def get_open_duels(user_chars: list):
    if not user_chars:
        return []

    worlds = list(set(char["world"] for char in user_chars))
    placeholders = ",".join("?" * len(worlds))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT creator_char, world, min_level, max_level, created_at
        FROM duels
        WHERE status = 'open'
        AND world IN ({placeholders})
        ORDER BY created_at DESC
    """, worlds)

    rows = cursor.fetchall()
    conn.close()

    duels = []
    for row in rows:
        duels.append({
            "creator_char": row[0],
            "world": row[1],
            "min_level": row[2],
            "max_level": row[3],
            "created_at": row[4],
        })

    return duels
