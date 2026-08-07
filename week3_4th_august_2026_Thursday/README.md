# Notes API

A RESTful Notes Management API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Alembic**, and **JWT Authentication**.

This project demonstrates a production-style backend architecture using:

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic Migrations
- JWT Authentication
- Role-Based Authorization (RBAC)
- Service Layer Architecture
- Docker & Docker Compose

---

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing using Passlib + Bcrypt

---

## Notes

- Create Note
- Get All Own Notes
- Get Note by ID
- Update Note
- Delete Note

Each note belongs to the authenticated user.

---

## Categories

- Create Category
- Get All Categories
- Get Category by ID
- Update Category
- Delete Category

Each category can have multiple notes.

---

## Admin

Admin-only endpoint:

```
GET /api/v1/admin/notes
```

Returns every user's notes.

---

# Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT (python-jose)
- Passlib
- Docker
- Docker Compose

---

# Project Structure

```
.
├── alembic/                     # Alembic migration files
│   ├── versions/
│   └── env.py
│
├── app/                         # Main application
│   ├── routers/                 # API routes
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── categories.py
│   │   └── notes.py
│   │
│   ├── services/                # Business logic
│   │   ├── auth_service.py
│   │   ├── category_service.py
│   │   └── note_service.py
│   │
│   ├── config.py                # Environment configuration
│   ├── database.py              # Database connection
│   ├── dependencies.py          # Authentication & authorization dependencies
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   └── security.py              # JWT & password utilities
│
├── frontend/                    # Minimal frontend for testing APIs
├── Images/                      # Project screenshots
│
├── .dockerignore
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

---

# Environment Variables

Copy the `.env.example` file to create a `.env` file and update it with your PostgreSQL credentials and application secrets.

**Windows**

```powershell
copy .env.example .env
```

**Linux/macOS**

```bash
cp .env.example .env
```

---

# Running with Docker (Recommended)

## Build

```bash
docker compose build
```

## Start

```bash
docker compose up
```

or

```bash
docker compose up --build
```

The application will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

> **Note:** Docker Compose starts both the FastAPI application and the PostgreSQL database automatically.

---

# Running Without Docker

## 1. Clone the Repository

```bash
git clone <repository-url>
```

```bash
cd <project-folder>
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create PostgreSQL Database

Using pgAdmin or psql, create a database named:

```
notes_db
```

---

## 5. Configure Environment Variables

Copy `.env.example` to `.env` and update it with your PostgreSQL credentials and application secrets.

---

## 6. Apply Alembic Migrations

```bash
alembic upgrade head
```

---

## 7. Start the Server

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Authentication Flow

1. Register a user

```
POST /api/v1/auth/register
```

2. Login

```
POST /api/v1/auth/login
```

3. Copy the generated JWT access token.

4. Click **Authorize** in Swagger.

5. Enter:

```
Bearer <your_token>
```

6. Access all protected endpoints.

---

# Main Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/auth/register` |
| POST | `/api/v1/auth/login` |

---

## Categories

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/categories` |
| GET | `/api/v1/categories` |
| GET | `/api/v1/categories/{id}` |
| PUT | `/api/v1/categories/{id}` |
| DELETE | `/api/v1/categories/{id}` |

---

## Notes

| Method | Endpoint |
|---------|----------|
| POST | `/api/v1/notes` |
| GET | `/api/v1/notes` |
| GET | `/api/v1/notes/{id}` |
| PUT | `/api/v1/notes/{id}` |
| DELETE | `/api/v1/notes/{id}` |

---

## Admin

| Method | Endpoint |
|---------|----------|
| GET | `/api/v1/admin/notes` |

---

# Database

The project uses **PostgreSQL** with **SQLAlchemy ORM**.

Database schema management is handled using **Alembic Migrations**.

### Main Entities

- User
- Note
- Category

### Relationships

```
User
 └── One-to-Many
      └── Notes

Category
 └── One-to-Many
      └── Notes
```

---

# Docker Commands

### Build

```bash
docker compose build
```

### Start

```bash
docker compose up
```

### Build & Start

```bash
docker compose up --build
```

### Run in Background

```bash
docker compose up -d
```

### Stop Containers

```bash
docker compose down
```

### Stop Containers and Remove Volumes

```bash
docker compose down -v
```

---

# Screenshots

Project screenshots can be found in the **Images/** directory.

---

# Author

**Muhammad Subhan**

AI/ML Intern @ ArhamSoft
