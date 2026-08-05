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
├── alembic/
├── app/
│   ├── routers/
│   ├── services/
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── database.py
│   ├── config.py
│   └── main.py
│
├── frontend/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# Environment Variables

Create a `.env` file in the project root.

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

The application will be available at

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

---

# Running Without Docker

## 1. Clone Repository

```bash
git clone <repository-url>
```

```bash
cd notes_api
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

Linux / macOS

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

Using pgAdmin or psql create a database:

```
notes_db
```

---

## 5. Configure Environment Variables

Create a `.env` file as shown above.

---

## 6. Apply Migrations

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

Swagger

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

3. Copy the access token.

4. Click **Authorize** in Swagger.

Enter:

```
Bearer <your_token>
```

5. Access protected endpoints.

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

The project uses PostgreSQL with SQLAlchemy ORM.

Schema management is handled using Alembic migrations.

Main entities:

- User
- Note
- Category

Relationships:

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

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

Run in background

```bash
docker compose up -d
```

Stop

```bash
docker compose down
```

Rebuild

```bash
docker compose up --build
```

---

# Author

**Muhammad Subhan**

AI/ML Intern @ ArhamSoft

Computer Science Student
