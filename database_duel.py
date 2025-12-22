import sqlite3

DB_NAME = "redmask.db"


def get_connection():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False,
        timeout=30
    )


# ===============================
# INICIALIZAÇÃO DAS TABELAS
# ===============================
def create_duel_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Duelos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS duels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_telegram_id INTEGER,
        creator_char TEXT,
        world TEXT,
        min_level INTEGER,
        max_level INTEGER,
        status TEXT DEFAULT 'open', -- open, accepted, finished, cancelled
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Participantes do duelo
    cur.execute("""
    CREATE TABLE IF NOT EXISTS duel_participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duel_id INTEGER,
        telegram_id INTEGER,
        char_name TEXT,
        accepted INTEGER DEFAULT 0,
        FOREIGN KEY (duel_id) REFERENCES duels (id)
    )
    """)

    # Histórico (log)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS duel_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duel_id INTEGER,
        message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ===============================
# CRIAR DUELO
# ===============================
def create_duel(telegram_id, char_name, world, min_level, max_level):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO duels
    (creator_telegram_id, creator_char, world, min_level, max_level)
    VALUES (?, ?, ?, ?, ?)
    """, (
        telegram_id,
        char_name,
        world,
        min_level,
        max_level
    ))

    duel_id = cur.lastrowid

    # Criador entra automaticamente como participante
    cur.execute("""
    INSERT INTO duel_participants
    (duel_id, telegram_id, char_name, accepted)
    VALUES (?, ?, ?, 1)
    """, (duel_id, telegram_id, char_name))

    conn.commit()
    conn.close()

    return duel_id


# ===============================
# LISTAR DUELOS ABERTOS (POR WORLD)
# ===============================
def get_open_duels(world):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, creator_char, min_level, max_level, created_at
    FROM duels
    WHERE status = 'open' AND world = ?
    ORDER BY created_at DESC
    """, (world,))

    duels = cur.fetchall()
    conn.close()
    return duels


# ===============================
# ENTRAR EM UM DUELO
# ===============================
def join_duel(duel_id, telegram_id, char_name):
    conn = get_connection()
    cur = conn.cursor()

    # Evita duplicação
    cur.execute("""
    SELECT id FROM duel_participants
    WHERE duel_id = ? AND telegram_id = ?
    """, (duel_id, telegram_id))

    if cur.fetchone():
        conn.close()
        return False

    cur.execute("""
    INSERT INTO duel_participants
    (duel_id, telegram_id, char_name)
    VALUES (?, ?, ?)
    """, (duel_id, telegram_id, char_name))

    conn.commit()
    conn.close()
    return True


# ===============================
# ACEITAR DUELO
# ===============================
def accept_duel(duel_id, telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE duel_participants
    SET accepted = 1
    WHERE duel_id = ? AND telegram_id = ?
    """, (duel_id, telegram_id))

    # Marca duelo como ativo
    cur.execute("""
    UPDATE duels
    SET status = 'accepted'
    WHERE id = ?
    """, (duel_id,))

    conn.commit()
    conn.close()


# ===============================
# FINALIZAR DUELO
# ===============================
def finish_duel(duel_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE duels
    SET status = 'finished'
    WHERE id = ?
    """, (duel_id,))

    conn.commit()
    conn.close()


# ===============================
# LOGS DO DUELO
# ===============================
def add_duel_log(duel_id, message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO duel_logs (duel_id, message)
    VALUES (?, ?)
    """, (duel_id, message))

    conn.commit()
    conn.close()


def get_duel_logs(duel_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT message, created_at
    FROM duel_logs
    WHERE duel_id = ?
    ORDER BY created_at ASC
    """, (duel_id,))

    logs = cur.fetchall()
    conn.close()
    return logs
