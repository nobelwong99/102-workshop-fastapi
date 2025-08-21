"""
FastAPI Task Management Application

A simple REST API for managing tasks with CRUD operations.
This application provides endpoints to create, read, update, and delete tasks.

Author: Nobel Wong - TM Technology
Date: 2025-08-21
"""

from fastapi import FastAPI
from pydantic import BaseModel


class Task(BaseModel):
    """
    Task model representing a task item.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Title/name of the task
        description (str): Detailed description of the task
        completed (bool): Status indicating if task is completed
            (default: False)
    """

    id: int
    title: str
    description: str
    completed: bool = False


# Initialize FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A simple API for managing tasks",
    version="1.0.0",
)

# In-memory storage for tasks
# (in production, use a proper database)
tasks = [
    {
        "id": 1,
        "title": "Task 1",
        "description": "Task 1 description",
        "completed": False,
    },
    {
        "id": 2,
        "title": "Task 2",
        "description": "Task 2 description",
        "completed": False,
    },
    {
        "id": 3,
        "title": "Task 3",
        "description": "Task 3 description",
        "completed": False,
    },
]


@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: Welcome message
    """
    return {"message": "Hello World"}


@app.get("/tasks")
def read_tasks():
    """
    Retrieve all tasks.

    Returns:
        dict: Dictionary containing all tasks
    """
    return {"tasks": tasks}


@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    """
    Retrieve a specific task by its ID.

    Args:
        task_id (int): The unique identifier of the task

    Returns:
        dict: Task data if found, or error message if not found
    """
    # Search for task with matching ID
    for task in tasks:
        if task["id"] == task_id:
            return {"message": "Task found", "task": task}

    # Return error if task not found
    return {"message": "Task not found"}


@app.post("/tasks")
def create_task(task: Task):
    """
    Create a new task.

    Args:
        task (Task): Task object containing task details

    Returns:
        dict: Confirmation message and created task data
    """
    # Convert Pydantic model to dictionary and add to tasks list
    tasks.append(task.model_dump())
    return {"message": "Task created", "task": task}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    """
    Update an existing task by its ID.

    Args:
        task_id (int): The unique identifier of the task to update
        updated_task (Task): Updated task data

    Returns:
        dict: Confirmation message and updated task data, or error if not found
    """
    # Search for task with matching ID and update its fields
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed
            return {"message": "Task updated", "task": task}

    # Return error if task not found
    return {"message": "Task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    Delete a task by its ID.

    Args:
        task_id (int): The unique identifier of the task to delete

    Returns:
        dict: Confirmation message and deleted task data, or error if not found
    """
    # Search for task with matching ID and remove it
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted", "task": task}

    # Return error if task not found
    return {"message": "Task not found"}
