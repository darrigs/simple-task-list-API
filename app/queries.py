import strawberry
from typing import List, Optional
from app.models import Task
from app.database import get_all_tasks, get_task_by_id

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, search: Optional[str] = None) -> List[Task]:
        return get_all_tasks(search)

    @strawberry.field
    def task(self, id: int) -> Optional[Task]:
        return get_task_by_id(id)