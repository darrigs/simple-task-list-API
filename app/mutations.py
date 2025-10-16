import strawberry
from typing import Optional
from app.models import Task
from app.database import add_task_to_db, toggle_task_status, delete_task_from_db

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> Task:
        return add_task_to_db(title)

    @strawberry.mutation
    def toggle_task(self, id: int) -> Optional[Task]:
        return toggle_task_status(id)

    @strawberry.mutation
    def delete_task(self, id: int) -> Optional[Task]:
        return delete_task_from_db(id)