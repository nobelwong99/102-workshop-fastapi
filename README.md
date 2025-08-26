# FastAPI Workshop Projects

A collection of FastAPI applications demonstrating REST API development patterns. This repository contains multiple projects showcasing different aspects of building APIs with FastAPI, from basic task management to complex movie review systems.

## Projects Overview

### 1. Task Manager API (`/task-manager/`)

A simple and efficient REST API for managing tasks with full CRUD operations.

**Features:**

- ✅ Create new tasks
- 📋 Retrieve all tasks or specific tasks by ID
- ✏️ Update existing tasks
- 🗑️ Delete tasks
- 🔍 Filter tasks by completion status
- 📚 Interactive API documentation with Swagger UI

### 2. Movie Review API (`/movie-review/`)

A comprehensive movie and review management system with advanced filtering and validation.

**Features:**

- 🎬 Complete movie CRUD operations
- ⭐ Review system with ratings (1.0-10.0)
- 🎭 Genre-based categorization
- 🔍 Advanced filtering (by genre, year, director, rating)
- 📊 Statistics and analytics endpoints
- 🎯 Automatic rating calculations
- 📱 Web dashboard interface

### 3. Hotel Booking API (`/bookings/`)

A comprehensive hotel management system for rooms and bookings with advanced features.

**Features:**

- 🏨 Complete hotel room management (CRUD operations)
- 📅 Booking system with date validation and availability checking
- 🔍 Advanced filtering and sorting for rooms and bookings
- 💰 Automatic price calculation and revenue tracking
- 📊 Hotel statistics and analytics dashboard
- 🏷️ Room type categorization (Single, Double, Suite, Deluxe, Presidential)
- ✅ Booking status management (Pending, Confirmed, Checked-in, Checked-out, Cancelled)
- 📱 Beautiful web interface for hotel management
- 🛡️ Comprehensive validation and error handling

### 4. Template Project (`/template/`)

A minimal FastAPI starter template for new projects.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and settings management
- **Python 3.8+** - Programming language
- **JSON** - File-based data storage for simplicity

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

## Running the Applications

### Task Manager API

```bash
cd task-manager
fastapi dev main.py
```

The Task Manager API will be available at `http://localhost:8000`

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Movie Review API

```bash
cd movie-review
fastapi dev movie_review_api.py
```

The Movie Review API will be available at `http://localhost:8000`

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Web Dashboard**: `movie_review_dashboard.html` (open in browser)

### Hotel Booking API

```bash
cd bookings
fastapi dev main.py
```

The Hotel Booking API will be available at `http://localhost:8000`

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Web Interface**: `index.html` (open in browser)

### Template Project

```bash
cd template
fastapi dev api.py
```

The Template API will be available at `http://localhost:8000`

## API Documentation

Each project includes interactive API documentation accessible once the server is running:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Task Manager API Endpoints

**Base URL:** `http://localhost:8000` (when running task-manager)

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

## Movie Review API Endpoints

**Base URL:** `http://localhost:8000` (when running movie-review)

### Movies

| Method | Endpoint       | Description               | Request Body |
| ------ | -------------- | ------------------------- | ------------ |
| GET    | `/movies`      | Get all movies (filtered) | None         |
| GET    | `/movies/{id}` | Get specific movie        | None         |
| POST   | `/movies`      | Create new movie          | Movie object |
| PUT    | `/movies/{id}` | Update existing movie     | Movie object |
| DELETE | `/movies/{id}` | Delete movie              | None         |

### Reviews

| Method | Endpoint        | Description            | Request Body  |
| ------ | --------------- | ---------------------- | ------------- |
| GET    | `/reviews`      | Get all reviews        | None          |
| GET    | `/reviews/{id}` | Get specific review    | None          |
| POST   | `/reviews`      | Create new review      | Review object |
| PUT    | `/reviews/{id}` | Update existing review | Review object |
| DELETE | `/reviews/{id}` | Delete review          | None          |

### Additional Endpoints

| Method | Endpoint               | Description               |
| ------ | ---------------------- | ------------------------- |
| GET    | `/movies/{id}/reviews` | Get all reviews for movie |
| GET    | `/stats`               | Get system statistics     |

## Hotel Booking API Endpoints

**Base URL:** `http://localhost:8000` (when running bookings)

### Rooms

| Method | Endpoint      | Description              | Request Body |
| ------ | ------------- | ------------------------ | ------------ |
| GET    | `/rooms`      | Get all rooms (filtered) | None         |
| GET    | `/rooms/{id}` | Get specific room        | None         |
| POST   | `/rooms`      | Create new room          | Room object  |
| PUT    | `/rooms/{id}` | Update existing room     | Room object  |
| DELETE | `/rooms/{id}` | Delete room              | None         |

### Bookings

| Method | Endpoint         | Description             | Request Body   |
| ------ | ---------------- | ----------------------- | -------------- |
| GET    | `/bookings`      | Get all bookings        | None           |
| GET    | `/bookings/{id}` | Get specific booking    | None           |
| POST   | `/bookings`      | Create new booking      | Booking object |
| PUT    | `/bookings/{id}` | Update existing booking | Booking object |
| DELETE | `/bookings/{id}` | Delete booking          | None           |

### Additional Hotel Endpoints

| Method | Endpoint                | Description               |
| ------ | ----------------------- | ------------------------- |
| PUT    | `/bookings/{id}/status` | Update booking status     |
| GET    | `/rooms/{id}/bookings`  | Get all bookings for room |
| GET    | `/rooms/availability`   | Check room availability   |
| GET    | `/stats`                | Get hotel statistics      |

## Example Requests

### Task Manager API Examples

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

#### Get Completed Tasks Only

```bash
curl -X GET "http://localhost:8000/tasks?completed=true"
```

### Movie Review API Examples

#### Create a Movie

```bash
curl -X POST "http://localhost:8000/movies" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "The Matrix",
       "description": "A sci-fi action film about reality and virtual worlds",
       "genre": "science_fiction",
       "release_year": 1999,
       "director": "The Wachowskis",
       "duration_minutes": 136
     }'
```

#### Get Movies by Genre

```bash
curl -X GET "http://localhost:8000/movies?genre=action&sort_by=rating&order=desc"
```

#### Create a Review

```bash
curl -X POST "http://localhost:8000/reviews" \
     -H "Content-Type: application/json" \
     -d '{
       "movie_id": 1,
       "reviewer_name": "John Doe",
       "rating": 8.5,
       "comment": "Amazing movie with great action sequences!"
     }'
```

### Hotel Booking API Examples

#### Create a Room

```bash
curl -X POST "http://localhost:8000/rooms" \
     -H "Content-Type: application/json" \
     -d '{
       "room_number": "201",
       "room_type": "double",
       "price_per_night": 200.0,
       "capacity": 2,
       "amenities": ["WiFi", "TV", "Air Conditioning", "Mini Bar"],
       "is_available": true,
       "description": "Comfortable double room with modern amenities"
     }'
```

#### Create a Booking

```bash
curl -X POST "http://localhost:8000/bookings" \
     -H "Content-Type: application/json" \
     -d '{
       "room_id": 1,
       "guest_name": "Alice Johnson",
       "guest_email": "alice@email.com",
       "check_in_date": "2025-02-01",
       "check_out_date": "2025-02-05",
       "num_guests": 2,
       "special_requests": "Late check-in preferred"
     }'
```

#### Check Room Availability

```bash
curl -X GET "http://localhost:8000/rooms/availability?check_in_date=2025-02-10&check_out_date=2025-02-15&num_guests=2&room_type=suite"
```

#### Get Hotel Statistics

```bash
curl -X GET "http://localhost:8000/stats"
```

## Development

### Running in Development Mode

All applications use the modern `fastapi dev` command which provides:

- Automatic reloading on file changes
- Built-in debugging capabilities
- Better error messages

```bash
# For any project
cd project-directory
fastapi dev filename.py
```

### Project Structure

```text
102-workshop-fastapi/
├── task-manager/
│   ├── main.py              # Task management API
│   ├── data.json            # Task data storage
│   ├── task_manager.html    # Frontend interface
│   └── test_api.py          # API tests
├── movie-review/
│   ├── movie_review_api.py       # Movie & review API
│   ├── movies.json               # Movie data storage
│   ├── reviews.json              # Review data storage
│   ├── movie_review_dashboard.html # Web dashboard
│   └── test_movie_api.py         # API tests
├── bookings/
│   ├── main.py              # Hotel booking API
│   ├── rooms.json           # Room data storage
│   ├── bookings.json        # Booking data storage
│   └── index.html           # Hotel management interface
├── template/
│   ├── api.py               # Basic FastAPI template
│   └── db.json              # Template data file
├── slides/                  # Workshop presentation materials
└── README.md               # This documentation
```

### Code Quality

All projects demonstrate best practices:

- **Comprehensive Documentation**: Detailed docstrings for all functions and classes
- **Type Hints**: Full type annotations for better code clarity
- **Pydantic Models**: Strong data validation and serialization
- **Error Handling**: Proper HTTP exceptions and status codes
- **CORS Support**: Cross-origin resource sharing enabled
- **Modular Design**: Clean separation of concerns

### Testing

Each project includes test files:

- `test_api.py` (Task Manager)
- `test_movie_api.py` (Movie Review)
- Test files for the Hotel Booking API can be created following the same patterns

Run tests using:

```bash
pytest test_api.py -v
```

## Features by Project

### Task Manager

- Basic CRUD operations
- Task filtering by completion status
- Auto-ID generation
- JSON file persistence

### Movie Review System

- Advanced movie management with genre validation
- Review system with rating calculations
- Complex filtering and sorting options
- Statistics and analytics
- Web dashboard interface
- Real-time rating updates

### Hotel Booking System

- Complete hotel room and booking management
- Advanced availability checking and date validation
- Price calculation and revenue tracking
- Multiple room types and booking statuses
- Statistical reporting and analytics
- Professional web interface for hotel staff

### Template

- Minimal FastAPI setup
- Basic JSON operations
- Perfect starting point for new projects

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Workshop Information

This repository contains materials from the FastAPI workshops:

- **Day 1**: Basic FastAPI concepts and Task Manager implementation
- **Day 2**: Advanced features with Movie Review system
- **Presentations**: Available in the `slides/` directory

## Author

**Nobel Wong** - TM Technology  
Workshop Date: 2025-08-21

## Learning Path

1. **Start with Template** (`/template/`) - Basic FastAPI setup
2. **Build Task Manager** (`/task-manager/`) - CRUD operations and filtering
3. **Explore Movie Review** (`/movie-review/`) - Advanced features and validation
4. **Master Hotel Booking** (`/bookings/`) - Complex business logic and data relationships

## Support

If you have any questions or need help with the projects:

- Review the interactive API documentation at `/docs`
- Check the test files for usage examples
- Open an issue on GitHub for bugs or feature requests

---

⭐ **Star this repository if you find it helpful!**

_Perfect for learning FastAPI development patterns and building RESTful APIs_
