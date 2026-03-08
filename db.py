"""Database module for Project Bridge - SQLite with concurrency handling."""

import sqlite3
import hashlib
import os
import time
import threading

DB_PATH = "project_bridge.db"
_lock = threading.Lock()


def get_connection():
    """Get a database connection with WAL mode enabled."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Simple SHA-256 hash for passwords."""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """Initialize database tables and seed users if needed."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            department_code TEXT,
            department_name TEXT,
            behavior_name TEXT,
            department_assigned_at TIMESTAMP,
            behavior_assigned_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Check if users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        default_password = hash_password("bridge2026")
        users = [
            ("director1", "Director 1"),
            ("director2", "Director 2"),
            ("director3", "Director 3"),
            ("director4", "Director 4"),
            ("director5", "Director 5"),
            ("director6", "Director 6"),
            ("director7", "Director 7"),
            ("director8", "Director 8"),
        ]
        for username, display_name in users:
            cursor.execute(
                "INSERT INTO users (username, password_hash, display_name) VALUES (?, ?, ?)",
                (username, default_password, display_name),
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO assignments (user_id) VALUES (?)",
                (user_id,),
            )

    conn.commit()
    conn.close()


def authenticate(username: str, password: str):
    """Authenticate user. Returns user dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, display_name FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password)),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row["id"], "username": row["username"], "display_name": row["display_name"]}
    return None


def get_assignment(user_id: int):
    """Get current assignment for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT department_code, department_name, behavior_name FROM assignments WHERE user_id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "department_code": row["department_code"],
            "department_name": row["department_name"],
            "behavior_name": row["behavior_name"],
        }
    return None


def get_taken_departments():
    """Get list of department codes already assigned."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT department_code FROM assignments WHERE department_code IS NOT NULL"
    )
    taken = [row["department_code"] for row in cursor.fetchall()]
    conn.close()
    return taken


def get_taken_behaviors():
    """Get list of behavior names already assigned."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT behavior_name FROM assignments WHERE behavior_name IS NOT NULL"
    )
    taken = [row["behavior_name"] for row in cursor.fetchall()]
    conn.close()
    return taken


def assign_department(user_id: int, department_code: str, department_name: str) -> bool:
    """
    Assign a department to a user atomically.
    Returns True if successful, False if department was already taken.
    """
    with _lock:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")

            # Check if user already has a department
            cursor.execute(
                "SELECT department_code FROM assignments WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row and row["department_code"] is not None:
                conn.rollback()
                return True  # Already assigned, that's fine

            # Check if department is still available
            cursor.execute(
                "SELECT COUNT(*) FROM assignments WHERE department_code = ?",
                (department_code,),
            )
            if cursor.fetchone()[0] > 0:
                conn.rollback()
                return False  # Already taken

            # Assign it
            cursor.execute(
                "UPDATE assignments SET department_code = ?, department_name = ?, department_assigned_at = datetime('now') WHERE user_id = ?",
                (department_code, department_name, user_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()


def assign_behavior(user_id: int, behavior_name: str) -> bool:
    """
    Assign a behavior to a user atomically.
    Returns True if successful, False if behavior was already taken.
    """
    with _lock:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")

            # Check if user already has a behavior
            cursor.execute(
                "SELECT behavior_name FROM assignments WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row and row["behavior_name"] is not None:
                conn.rollback()
                return True  # Already assigned

            # Check if behavior is still available
            cursor.execute(
                "SELECT COUNT(*) FROM assignments WHERE behavior_name = ?",
                (behavior_name,),
            )
            if cursor.fetchone()[0] > 0:
                conn.rollback()
                return False  # Already taken

            # Assign it
            cursor.execute(
                "UPDATE assignments SET behavior_name = ?, behavior_assigned_at = datetime('now') WHERE user_id = ?",
                (behavior_name, user_id),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()


def get_all_assignments():
    """Get all assignments for the admin panel."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.display_name, u.username, a.department_code, a.department_name, 
               a.behavior_name, a.department_assigned_at, a.behavior_assigned_at
        FROM users u
        JOIN assignments a ON u.id = a.user_id
        ORDER BY u.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def reset_all():
    """Reset all assignments for a new round."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE assignments 
        SET department_code = NULL, department_name = NULL, 
            behavior_name = NULL, department_assigned_at = NULL, 
            behavior_assigned_at = NULL
    """)
    conn.commit()
    conn.close()


def get_progress():
    """Get overall progress stats."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM assignments WHERE department_code IS NOT NULL")
    dept_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM assignments WHERE behavior_name IS NOT NULL")
    behav_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()
    return {"departments_assigned": dept_count, "behaviors_assigned": behav_count, "total": total}


# Initialize on import
init_db()
