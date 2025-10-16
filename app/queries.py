import strawberry
from typing import List, Optional
from app.models import Task
from app.database import get_all_tasks, get_task_by_id

def row_to_task(row) -> Task:
    return Task(
        id=row[0],
        title=row[1],
        completed=bool(row[2]),
        created_at=row[3],
        updated_at=row[4]
    )

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, search: Optional[str] = None) -> List[Task]:
        rows = get_all_tasks(search)
        return [row_to_task(row) for row in rows]

    @strawberry.field
    def task(self, id: int) -> Optional[Task]:
        row = get_task_by_id(id)
        return row_to_task(row) if row else None