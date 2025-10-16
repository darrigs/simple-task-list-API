import sqlite3
from datetime import datetime
from typing import List, Optional
from app.models import Task, row_to_task

DB_PATH = "tasks.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()

def add_task_to_db(title: str) -> Task:
    now = datetime.utcnow().isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, completed, created_at, updated_at) VALUES (?, 0, ?, ?)",
            (title, now, now)
        )
        task_id = cur.lastrowid
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return row_to_task(row)

def get_all_tasks(search: Optional[str] = None) -> List[Task]:
    with get_connection() as conn:
        if search:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE title LIKE ? ORDER BY created_at DESC",
                (f"%{search}%",)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC"
            ).fetchall()
        return [row_to_task(row) for row in rows]

def get_task_by_id(task_id: int) -> Optional[Task]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return row_to_task(row) if row else None

def toggle_task_status(task_id: int) -> Optional[Task]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            return None
        completed = 0 if row[2] else 1
        now = datetime.utcnow().isoformat()
        conn.execute(
            "UPDATE tasks SET completed = ?, updated_at = ? WHERE id = ?",
            (completed, now, task_id)
        )
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return row_to_task(row)

def delete_task_from_db(task_id: int) -> Optional[Task]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            return None
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return row_to_task(row)