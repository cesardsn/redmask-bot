import sqlite3
from database import get_connection


def create_duel_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenger_char TEXT,
        target_char TEXT,
        world TEXT,
        min_level INTEGER,
        max_level INTEGER,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_duel(challenger, world, min_lvl, max_lvl):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO duels
    (challenger_char, world, min_level, max_level, status, created_at)
    VALUES (?, ?, ?, ?, 'OPEN', datetime('now'))
    """, (challenger, world, min_lvl, max_lvl))

    conn.commit()
    conn.close()


def accept_duel(duel_id, target_char):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE duels
    SET target_char=?, status='ACCEPTED'
    WHERE id=?
    """, (target_char, duel_id))

    conn.commit()
    conn.close()


def get_open_duels(world, level):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, challenger_char, min_level, max_level
    FROM duels
    WHERE status='OPEN'
    AND world=?
    AND ? BETWEEN min_level AND max_level
    """, (world, level))

    rows = cur.fetchall()
    conn.close()
    return rows
