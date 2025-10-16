import strawberry
from typing import Optional
from app.models import Task
from app.database import add_task_to_db, toggle_task_status, delete_task_from_db
from app.queries import row_to_task

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> Optional[Task]:
        if not title or len(title.strip()) < 1:
            raise Exception("Task title must be at least 1 character long.")
        row = add_task_to_db(title)
        if not row:
            return None
        return row_to_task(row)

    @strawberry.mutation
    def toggle_task(self, id: int) -> Optional[Task]:
        row = toggle_task_status(id)
        if not row:
            return None
        return row_to_task(row)

    @strawberry.mutation
    def delete_task(self, id: int) -> Optional[Task]:
        row = delete_task_from_db(id)
        if not row:
            return None
        return row_to_task(row)