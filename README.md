# FastAPI Task Management API

A simple and efficient REST API for managing tasks built with FastAPI. This application provides full CRUD (Create, Read, Update, Delete) operations for task management.

## Features

- ✅ Create new tasks
- 📋 Retrieve all tasks or specific tasks by ID
- ✏️ Update existing tasks
- 🗑️ Delete tasks
- 📚 Interactive API documentation with Swagger UI
- 🔍 Automatic request/response validation
- 🚀 High-performance async API

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and settings management
- **Python 3.8+** - Programming language

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**

   ```bash
   git clone <your-repository-url>
   cd 102-workshop-fastapi
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install "fastapi[standard]"
   ```

4. **Run the application**
   ```bash
   fastapi dev main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### Base URL: `http://localhost:8000`

| Method | Endpoint           | Description          | Request Body |
| ------ | ------------------ | -------------------- | ------------ |
| GET    | `/`                | Welcome message      | None         |
| GET    | `/tasks`           | Get all tasks        | None         |
| GET    | `/tasks/{task_id}` | Get specific task    | None         |
| POST   | `/tasks`           | Create new task      | Task object  |
| PUT    | `/tasks/{task_id}` | Update existing task | Task object  |
| DELETE | `/tasks/{task_id}` | Delete task          | None         |

### Task Model

```json
{
	"id": 1,
	"title": "Task Title",
	"description": "Task description",
	"completed": false
}
```

### Example Requests

#### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "id": 4,
       "title": "New Task",
       "description": "This is a new task",
       "completed": false
     }'
```

#### Get All Tasks

```bash
curl -X GET "http://localhost:8000/tasks"
```

#### Get Specific Task

```bash
curl -X GET "http://localhost:8000/tasks/1"
```

#### Update a Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "id": 1,
       "title": "Updated Task",
       "description": "This task has been updated",
       "completed": true
     }'
```

#### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

### Response Examples

#### Successful Task Creation

```json
{
	"message": "Task created",
	"task": {
		"id": 4,
		"title": "New Task",
		"description": "This is a new task",
		"completed": false
	}
}
```

#### Task Not Found

```json
{
	"message": "Task not found"
}
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure

```
fastapi/
├── main.py          # Main application file
├── README.md        # Project documentation
└── requirements.txt # Dependencies (if created)
```

### Code Quality

The codebase includes:

- Comprehensive docstrings for all functions and classes
- Type hints for better code clarity
- Pydantic models for data validation
- Proper error handling

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] Task priority levels
- [ ] Search and filtering capabilities
- [ ] Unit and integration tests
- [ ] Docker containerization
- [ ] API rate limiting
- [ ] Logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Nobel Wong** - TM Technology  
Date: 2025-08-21

## Support

If you have any questions or need help with the project, please open an issue on GitHub.

---

⭐ **Star this repository if you find it helpful!**
