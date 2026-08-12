# ArhamSoft Notes

A full-stack **Notes** application:

- **Backend:** FastAPI + PostgreSQL + SQLAlchemy + Alembic + JWT
- **Frontend:** React (Vite) + JavaScript/JSX + CSS
- **Infra:** Docker & Docker Compose

Users can register/login, manage their own notes and categories, and admins can view all notes.

---

## Features

- JWT authentication (register + login)
- Notes CRUD (create, list, get by id, update, delete)
- Categories CRUD (per-user ownership)
- Category filter on notes
- Role-based admin endpoint (`GET /api/v1/admin/notes`)
- CORS enabled for the React app (`http://localhost:5173`)
- Alembic migrations on Docker startup
- Dockerized backend, database, and frontend

---

## Tech stack

| Layer | Technologies |
|-------|----------------|
| Backend | FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, Passlib/Bcrypt |
| Frontend | React, Vite, JavaScript/JSX, CSS |
| Containers | Docker, Docker Compose, nginx (frontend image) |

---

## Project structure

```
.
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── ...
│   ├── alembic.ini
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── nginx.conf
│
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Prerequisites

### With Docker (recommended)

- Docker Desktop installed and running

### Without Docker

- Python 3.13+
- Node.js 20+ (npm)
- PostgreSQL running locally

---

## Environment variables

### Root `.env` (backend + database)

**Windows**

```powershell
copy .env.example .env
```

**Linux/macOS**

```bash
cp .env.example .env
```

Example values:

```env
DATABASE_URL=postgresql+psycopg://postgres:yourpassword@localhost:5432/notes_db

POSTGRES_DB=notes_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Notes:

- For **local uvicorn** (no Docker API), keep `DATABASE_URL` with host `localhost`.
- For **Docker Compose**, the API service overrides `DATABASE_URL` to use host `db` automatically.
- Never commit `.env` (it is gitignored). Keep `.env.example` with dummy values only.

### Frontend `.env` (local Vite only)

Needed only when running the frontend with `npm run dev`:

```powershell
copy frontend\.env.example frontend\.env
```

```env
VITE_API_URL=http://localhost:8000
```

When the frontend is built in Docker, `VITE_API_URL` is passed as a build arg (`http://localhost:8000`).

---

## Option A — Run everything with Docker

This starts **PostgreSQL**, **FastAPI**, and the **React frontend** together.

### 1. Start Docker Desktop

Wait until Docker Desktop shows it is running.

### 2. Open the project root

```powershell
cd path\to\week3_4th_august_2026_Thursday
```

### 3. Create `.env`

```powershell
copy .env.example .env
```

Update `POSTGRES_*`, `SECRET_KEY`, and related values.

> If a local PostgreSQL is already using port **5432**, stop it first or Docker’s Postgres container may fail to bind.

### 4. Build and start

```powershell
docker compose up --build
```

Detached mode:

```powershell
docker compose up --build -d
```

### 5. Open the apps

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### Useful Docker commands

```powershell
docker compose ps
docker compose logs -f
docker compose logs -f api
docker compose logs -f frontend
docker compose down
docker compose down -v
```

`down -v` also deletes the Postgres volume (all DB data).

---

## Option B — Run without Docker

### 1. Backend setup

From the project root:

**Windows**

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. PostgreSQL

Create a database named `notes_db` (or matching `POSTGRES_DB`).

Ensure root `.env` uses `localhost`:

```env
DATABASE_URL=postgresql+psycopg://postgres:yourpassword@localhost:5432/notes_db
```

### 3. Run migrations and start the API

```powershell
cd backend
alembic upgrade head
uvicorn app.main:app --reload
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

### 4. Frontend setup (second terminal)

```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```

Frontend: http://localhost:5173

---

## Option C — Hybrid

Run **database + API in Docker**, frontend with local Vite:

```powershell
docker compose up --build db api
```

Then:

```powershell
cd frontend
npm install
npm run dev
```

---

## Authentication flow

1. **Sign up** in the UI (or `POST /api/v1/auth/register`)
2. **Sign in** (`POST /api/v1/auth/login`)
3. Use the returned JWT:

```http
Authorization: Bearer <access_token>
```

The React app stores the token in `localStorage` as `access_token`.

### Testing the admin endpoint

New users get `role="user"`. Promote a user in PostgreSQL:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'your-email@example.com';
```

Log out and log in again. The **Admin** nav item appears and calls `GET /api/v1/admin/notes`.

---

## Main API endpoints

### Authentication

| Method | Endpoint |
|--------|----------|
| POST | `/api/v1/auth/register` |
| POST | `/api/v1/auth/login` |

### Categories (owned by the logged-in user)

| Method | Endpoint |
|--------|----------|
| POST | `/api/v1/categories` |
| GET | `/api/v1/categories` |
| GET | `/api/v1/categories/{id}` |
| PUT | `/api/v1/categories/{id}` |
| DELETE | `/api/v1/categories/{id}` |

### Notes (owned by the logged-in user)

| Method | Endpoint |
|--------|----------|
| POST | `/api/v1/notes` |
| GET | `/api/v1/notes` |
| GET | `/api/v1/notes/{id}` |
| PUT | `/api/v1/notes/{id}` |
| DELETE | `/api/v1/notes/{id}` |

### Admin

| Method | Endpoint |
|--------|----------|
| GET | `/api/v1/admin/notes` |

---

## Frontend overview

- Login / Sign up against the real API
- Notes CRUD with loading, empty, success, and error states
- Categories page (create / edit / delete)
- Category dropdown when creating/editing notes
- Local React state updates after create/update/delete (no full-list refetch)
- White + orange professional UI
- Responsive layout

---

## Ownership rules

- Each user only sees and manages **their own notes**
- Each user only sees and manages **their own categories**
- Notes can only be assigned to categories owned by the same user
- Admins can list all notes via `/api/v1/admin/notes`

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| Docker can’t start Postgres | Stop local PostgreSQL using port `5432`, or change the compose port mapping |
| CORS / `net::ERR_FAILED` on API calls | Usually a backend 500 or dead server. Check `docker compose logs -f api` or your uvicorn terminal |
| Frontend can’t reach API | Confirm API is on http://localhost:8000 and `VITE_API_URL` is `http://localhost:8000` |
| Stale Docker frontend after code changes | Rebuild: `docker compose up --build frontend` |
| Alembic / schema errors | From `backend/`: `alembic upgrade head` |
| Port already in use (`8000` / `5173`) | Stop the old process or change the published ports in `docker-compose.yml` |
| Multiple uvicorn instances | Keep only one API process on port `8000` |

---

## Author

**Muhammad Subhan**

AI/ML Intern @ ArhamSoft
