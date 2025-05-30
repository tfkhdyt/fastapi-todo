# FastAPI Todo App

A modern, async Todo application built with FastAPI, SQLModel, and SQLite. This project provides a RESTful API for managing tasks with user authentication and authorization.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication system
- **User Registration**: Sign up with username and password
- **Task Management**: Full CRUD operations for todo tasks
- **User Authorization**: Users can only access their own tasks
- **Async Operations**: Fully asynchronous database operations
- **Database Migrations**: Managed with Alembic
- **Configuration Management**: YAML-based configuration
- **Error Handling**: Comprehensive error handling and logging
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for Python
- **Database ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) - SQLAlchemy-based ORM with Pydantic integration
- **Database**: SQLite (async with aiosqlite)
- **Authentication**: JWT tokens with passlib for password hashing
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) for database schema management
- **Configuration**: Pydantic Settings with YAML support
- **Package Management**: [UV](https://github.com/astral-sh/uv) for fast Python package management

## 📋 Prerequisites

- Python 3.13+
- UV package manager (recommended) or pip

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-todo
```

### 2. Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Create virtual environment and install dependencies

```bash
uv sync
```

### 4. Set up configuration

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` and update the JWT secret key:

```yaml
database:
  sqlite:
    file_name: "database.db"

jwt:
  secret_key: "your-super-secret-jwt-key-here" # Change this!
  algorithm: "HS256"
  access_token_expire_minutes: 30
```

### 5. Run database migrations

```bash
uv run alembic upgrade head
```

### 6. Start the development server

```bash
uv run fastapi dev app/main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Register a new user via `POST /auth/sign-up`
2. Login via `POST /token` to get an access token
3. Include the token in the `Authorization` header: `Bearer <your-token>`

## 📖 API Endpoints

### Authentication

| Method | Endpoint        | Description                | Authentication |
| ------ | --------------- | -------------------------- | -------------- |
| POST   | `/auth/sign-up` | Register a new user        | No             |
| POST   | `/token`        | Login and get access token | No             |
| GET    | `/auth/me`      | Get current user info      | Yes            |

### Tasks

| Method | Endpoint           | Description          | Authentication |
| ------ | ------------------ | -------------------- | -------------- |
| GET    | `/tasks`           | Get all user's tasks | Yes            |
| POST   | `/tasks`           | Create a new task    | Yes            |
| GET    | `/tasks/{task_id}` | Get a specific task  | Yes            |
| PATCH  | `/tasks/{task_id}` | Update a task        | Yes            |
| DELETE | `/tasks/{task_id}` | Delete a task        | Yes            |

### Health Check

| Method | Endpoint  | Description       | Authentication |
| ------ | --------- | ----------------- | -------------- |
| GET    | `/health` | API health status | No             |

## 💾 Database Schema

### Users Table

- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Tasks Table

- `id`: Primary key
- `title`: Task title
- `description`: Task description (optional)
- `is_completed`: Completion status
- `user_id`: Foreign key to users table
- `created_at`: Timestamp
- `updated_at`: Timestamp

## 🔧 Development

### Creating Database Migrations

```bash
uv run alembic revision --autogenerate -m "Description of changes"
uv run alembic upgrade head
```

## 📝 Example Usage

### Register a new user

```bash
curl -X POST "http://localhost:8000/auth/sign-up" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Login

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

### Create a task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"title": "Learn FastAPI", "description": "Study FastAPI documentation"}'
```

### Get all tasks

```bash
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer <your-token>"
```

## 📁 Project Structure

```
fastapi-todo/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routers/               # API route handlers
│   │   ├── auth.py           # Authentication endpoints
│   │   └── tasks.py          # Task management endpoints
│   └── internal/             # Internal modules
│       ├── models/           # Data models
│       │   ├── user.py       # User model and schemas
│       │   ├── task.py       # Task model and schemas
│       │   └── jwt.py        # JWT token schemas
│       ├── db.py             # Database connection and session
│       ├── security.py       # Authentication and security utilities
│       ├── settings.py       # Configuration management
│       └── validators.py     # Custom validators
├── alembic/                  # Database migrations
│   └── versions/             # Migration files
├── config.yaml               # Application configuration
├── config.example.yaml       # Configuration template
├── pyproject.toml           # Project dependencies and metadata
├── uv.lock                  # Locked dependencies
└── README.md                # This file
```

## 🎯 Next Steps / TODO

- [ ] Add task categories/tags
- [ ] Implement task due dates
- [ ] Add task priority levels
- [ ] Implement task sharing between users
- [ ] Add pagination for task listings
- [ ] Implement task search and filtering
- [ ] Add email notifications
- [ ] Create a frontend application
- [ ] Add comprehensive test suite
- [ ] Set up CI/CD pipeline
