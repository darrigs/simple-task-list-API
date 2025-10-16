# simple-task-list-API

## Overview

This is a simple FastAPI application using Strawberry GraphQL and SQLite for a task list.

---

## Installation

1. **Clone the repository** (if you haven't already):

    ```bash
    git clone <your-repo-url>
    cd simple-task-list-API
    ```

2. **Create and activate a virtual environment** (recommended):

    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---

## Running the App

1. **Initialize the database** (optional, handled automatically on first run):

    ```bash
    python -c "from app.database import init_db; init_db()"
    ```

2. **Start the FastAPI server:**

    ```bash
    uvicorn app.main:app --reload
    ```

3. **Access the app:**

    - Home: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - GraphQL Playground: [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)

---

## GraphQL API

### Main Operations

- **Query: `tasks(search: String)`**  
  Returns a list of all tasks, optionally filtered by title.

- **Query: `task(id: ID!)`**  
  Returns a single task by its ID, or `null` if not found.

- **Mutation: `add_task(title: String!)`**  
  Creates a new task.

- **Mutation: `toggle_task(id: ID!)`**  
  Toggles the completed status of a task.

- **Mutation: `delete_task(id: ID!)`**  
  Deletes a task by its ID.

---

## Error Handling

- All errors are handled gracefully.  
- If a task is not found (e.g., toggling or deleting a non-existent task), the mutation returns `null` and does not crash the server.
- Database errors are caught and logged to the console.
- For more complex error scenarios (e.g., database connection loss, malformed input), you can:
    - Add custom error messages using Strawberry’s `@strawberry.field` or `@strawberry.mutation` with `raise Exception("...")`.
    - Use FastAPI exception handlers for global error handling.
    - Log errors to a file or monitoring service for production use.

**Example for more complex error handling:**
```python
@strawberry.mutation
def add_task(self, title: str) -> Optional[Task]:
    if not title or len(title) < 3:
        raise Exception("Title must be at least 3 characters long.")
    try:
        row = insert_task(title)
        return row_to_task(row)
    except Exception as e:
        # Log error, return None or raise a user-friendly error
        raise Exception("Failed to add task due to a server error.")
```

---

## Suggested Additional Queries/Mutations

1. **Update Task Title**
    ```graphql
    mutation {
      update_task_title(id: 1, title: "New Title") {
        id
        title
        completed
        updated_at
      }
    }
    ```
    *Updates the title of an existing task.*

2. **Mark All Tasks as Completed**
    ```graphql
    mutation {
      complete_all_tasks {
        id
        title
        completed
      }
    }
    ```
    *Marks all tasks as completed.*

---

## API Docs

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## License

MIT