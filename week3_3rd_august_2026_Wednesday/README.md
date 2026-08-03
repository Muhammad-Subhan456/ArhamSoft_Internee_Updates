# Task API with SQLAlchemy

## Features
- FastAPI
- SQLAlchemy ORM
- SQLite
- Alembic Migrations
- API Key Authentication
- Category–Task Relationship

## Installation

pip install -r requirements.txt

## Run

uvicorn app.main:app --reload

## Docker

docker build -t task-api .
docker run -p 8000:8000 task-api

## API Documentation

http://localhost:8000/docs

## Database Migrations

alembic upgrade head
alembic downgrade -1