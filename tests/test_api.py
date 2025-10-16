from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_and_get_task():
    mutation = """
    mutation {
        addTask(title: "Test Task") {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    task = response.json()["data"]["addTask"]
    assert task["title"] == "Test Task"
    assert task["completed"] is False
    assert task["id"] is not None

    # Get the task by ID
    query = f"""
    query {{
        task(id: {task['id']}) {{
            id
            title
            completed
            createdAt
            updatedAt
        }}
    }}
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    fetched_task = response.json()["data"]["task"]
    assert fetched_task["id"] == task["id"]
    assert fetched_task["title"] == "Test Task"

def test_tasks_query_with_search():
    # Add two tasks
    client.post("/graphql", json={"query": 'mutation { addTask(title: "Alpha Task") { id } }'})
    client.post("/graphql", json={"query": 'mutation { addTask(title: "Beta Task") { id } }'})

    # Query all tasks
    query = """
    query {
        tasks {
            title
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    titles = [t["title"] for t in response.json()["data"]["tasks"]]
    assert "Alpha Task" in titles
    assert "Beta Task" in titles

    # Query with search
    query = """
    query {
        tasks(search: "Alpha") {
            title
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    titles = [t["title"] for t in response.json()["data"]["tasks"]]
    assert "Alpha Task" in titles
    assert "Beta Task" not in titles

def test_toggle_task_and_delete_task():
    # Add a task
    mutation = """
    mutation {
        addTask(title: "Toggle Me") {
            id
            completed
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    task_id = response.json()["data"]["addTask"]["id"]

    # Toggle the task
    mutation = f"""
    mutation {{
        toggleTask(id: {task_id}) {{
            id
            completed
        }}
    }}
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    toggled = response.json()["data"]["toggleTask"]
    assert toggled["completed"] is True

    # Toggle again
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    toggled = response.json()["data"]["toggleTask"]
    assert toggled["completed"] is False

    # Delete the task
    mutation = f"""
    mutation {{
        deleteTask(id: {task_id}) {{
            id
        }}
    }}
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    deleted = response.json()["data"]["deleteTask"]
    assert deleted["id"] == task_id

    # Ensure task is deleted
    query = f"""
    query {{
        task(id: {task_id}) {{
            id
        }}
    }}
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["task"] is None

def test_query_nonexistent_task_and_delete_nonexistent_task():
    # Query a non-existent task
    query = """
    query {
        task(id: 999999) {
            id
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["task"] is None

    # Delete a non-existent task
    mutation = """
    mutation {
        deleteTask(id: 999999) {
            id
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    assert response.json()["data"]["deleteTask"] is None

def test_add_task_invalid_input():
    # Try to add a task with an empty title
    mutation = """
    mutation {
        addTask(title: "") {
            id
            title
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    # Should return an error in the GraphQL response
    assert response.status_code == 200
    assert response.json().get("data", {}).get("addTask") is None
    assert "errors" in response.json()