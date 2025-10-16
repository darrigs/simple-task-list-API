import sqlite3
from datetime import datetime
from typing import List, Optional
from app.models import Task, row_to_task

DB_PATH = "tasks.db"

def get_connection():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

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

def add_task_to_db(title: str) -> Task:
    now = datetime.utcnow()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, completed, created_at, updated_at) VALUES (?, 0, ?, ?)",
                (title, now, now)
            )
            conn.commit()
            return get_task_by_id(cursor.lastrowid)
    except Exception as e:
        print(f"Error inserting task: {e}")
        return None

def get_all_tasks(search: Optional[str] = None) -> List[Task]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if search:
                cursor.execute("SELECT * FROM tasks WHERE title LIKE ? ORDER BY created_at DESC", (f"%{search}%",))
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return [row_to_task(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def get_task_by_id(task_id: int) -> Optional[Task]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return row_to_task(row) if row else None
    except Exception as e:
        print(f"Error fetching task by id: {e}")
        return None

def toggle_task_status(task_id: int) -> Optional[Task]:
    now = datetime.utcnow()
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
            return get_task_by_id(task_id)
    except Exception as e:
        print(f"Error toggling task: {e}")
        return None

def delete_task_from_db(task_id: int) -> Optional[Task]:
    try:
        task = get_task_by_id(task_id)
        if not task:
            return None
        with get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
        return task
    except Exception as e:
        print(f"Error deleting task: {e}")
        return None