import strawberry
from datetime import datetime

@strawberry.type
class Task:
    id: int
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

def row_to_task(row) -> Task:
    return Task(
        id=row[0],
        title=row[1],
        completed=bool(row[2]),
        created_at=row[3],
        updated_at=row[4]
    )