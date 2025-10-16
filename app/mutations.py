import strawberry
from typing import Optional
from app.models import Task
from app.database import insert_task, update_task_toggle, delete_task
from app.queries import row_to_task

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> Optional[Task]:
        row = insert_task(title)
        if not row:
            return None
        return row_to_task(row)

    @strawberry.mutation
    def toggle_task(self, id: int) -> Optional[Task]:
        row = update_task_toggle(id)
        if not row:
            return None
        return row_to_task(row)

    @strawberry.mutation
    def delete_task(self, id: int) -> Optional[Task]:
        row = delete_task(id)
        if not row:
            return None
        return row_to_task(row)