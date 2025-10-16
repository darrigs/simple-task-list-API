import sqlite3
from datetime import datetime, timezone
from typing import List, Optional
from app.models import Task, row_to_task

DB_PATH = "tasks.db"

# Register adapter and converter for TIMESTAMP
sqlite3.register_adapter(datetime, lambda dt: dt.isoformat(" "))
sqlite3.register_converter("TIMESTAMP", lambda s: datetime.fromisoformat(s.decode()))

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )

def init_db():
    try:
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
            """)
            conn.commit()
    except Exception as e:
        print(f"Database initialization failed: {e}")

def add_task_to_db(title: str):
    now = datetime.now(timezone.utc)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, completed, created_at, updated_at) VALUES (?, 0, ?, ?)",
                (title, now, now)
            )
            conn.commit()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error inserting task: {e}")
        return None

def get_all_tasks(search: Optional[str] = None):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if search:
                cursor.execute("SELECT * FROM tasks WHERE title LIKE ?", (f"%{search}%",))
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def get_task_by_id(task_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching task by id: {e}")
        return None

def toggle_task_status(task_id: int):
    now = datetime.now(timezone.utc)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if not row:
                return None
            new_completed = not bool(row[0])
            cursor.execute(
                "UPDATE tasks SET completed = ?, updated_at = ? WHERE id = ?",
                (new_completed, now, task_id)
            )
            conn.commit()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error toggling task: {e}")
        return None

def delete_task_from_db(task_id: int):
    try:
        task_row = get_task_by_id(task_id)
        if not task_row:
            return None
        with get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        return task_row
    except Exception as e:
        print(f"Error deleting task: {e}")
        return None