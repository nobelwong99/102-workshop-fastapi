"""
FastAPI Task Management Application

A simple REST API for managing tasks with CRUD operations.
This application provides endpoints to create, read, update, and delete tasks.

Author: Nobel Wong - TM Technology
Date: 2025-08-21
"""

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
import json
import os

TASK_NOT_FOUND_MESSAGE = "Task not found"
DATA_FILE = "data.json"


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


# Load tasks from JSON file
def load_data_from_json():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Error reading data from JSON file: {e}")
        return []


# Save tasks to JSON file
def save_data_to_json(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: Welcome message
    """
    return {"message": "Hello World"}


@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks(
    completed: Optional[bool] = Query(
        None, description="Filter tasks by completion status"
    ),
):
    """
    Retrieve all tasks with optional filtering.

    Args:
        completed (Optional[bool]): Filter tasks by completion status.
                                  If None, returns all tasks.

    Returns:
        dict: Dictionary containing filtered tasks
    """
    # Load tasks from JSON file
    tasks = load_data_from_json()

    # Start with all tasks
    filtered_tasks = tasks.copy()

    # Filter by completion status if specified
    if completed is not None:
        filtered_tasks = [
            task for task in filtered_tasks if task["completed"] == completed
        ]

    return {"tasks": filtered_tasks}


@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def read_task(task_id: int):
    """
    Retrieve a specific task by its ID.

    Args:
        task_id (int): The unique identifier of the task

    Returns:
        dict: Task data if found

    Raises:
        HTTPException: 404 if task not found
    """
    # Load tasks from JSON file
    tasks = load_data_from_json()

    # Search for task with matching ID
    for task in tasks:
        if task["id"] == task_id:
            return {"message": "Task found", "task": task}

    # Raise HTTP 404 exception if task not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND_MESSAGE
    )


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(
    task: Task,
    auto_id: bool = Query(False, description="Automatically generate task ID"),
):
    """
    Create a new task.

    Args:
        task (Task): Task object containing task details
                auto_id (bool): If True, automatically generates a unique ID,
                       ignoring the ID in the request body

    Returns:
        dict: Confirmation message and created task data

    Raises:
        HTTPException: 400 if task with same ID already exists
                       (when auto_id=False)
    """
    # Load tasks from JSON file
    tasks = load_data_from_json()

    # Handle auto ID generation
    if auto_id:
        # Generate new ID (find max ID and add 1)
        max_id = max([t["id"] for t in tasks], default=0)
        task.id = max_id + 1
    else:
        # Check if task with same ID already exists
        for existing_task in tasks:
            if existing_task["id"] == task.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Task with ID {task.id} already exists",
                )

    # Convert Pydantic model to dictionary and add to tasks list
    tasks.append(task.model_dump())

    # Save updated tasks back to JSON file
    save_data_to_json(tasks)

    return {"message": "Task created", "task": task}


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, updated_task: Task):
    """
    Update an existing task by its ID.

    Args:
        task_id (int): The unique identifier of the task to update
        updated_task (Task): Updated task data

    Returns:
        dict: Confirmation message and updated task data

    Raises:
        HTTPException: 404 if task not found
        HTTPException: 400 if trying to change task ID to existing ID
    """
    # Load tasks from JSON file
    tasks = load_data_from_json()

    # Check if trying to change ID to an existing one
    # (but not the current task)
    if updated_task.id != task_id:
        for task in tasks:
            if task["id"] == updated_task.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Task with ID {updated_task.id} already exists",
                )

    # Search for task with matching ID and update its fields
    for task in tasks:
        if task["id"] == task_id:
            task["id"] = updated_task.id
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed

            # Save updated tasks back to JSON file
            save_data_to_json(tasks)

            return {"message": "Task updated", "task": task}

    # Raise HTTP 404 exception if task not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND_MESSAGE
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    """
    Delete a task by its ID.

    Args:
        task_id (int): The unique identifier of the task to delete

    Returns:
        dict: Confirmation message and deleted task data

    Raises:
        HTTPException: 404 if task not found
    """
    # Load tasks from JSON file
    tasks = load_data_from_json()

    # Search for task with matching ID and remove it
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            # Save updated tasks back to JSON file
            save_data_to_json(tasks)

            return {"message": "Task deleted", "task": task}

    # Raise HTTP 404 exception if task not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND_MESSAGE
    )
