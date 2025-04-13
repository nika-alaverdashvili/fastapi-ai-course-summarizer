# FastAPI AI Course Summarizer

## Introduction

The **FastAPI AI Course Summarizer** is a high-performance REST API built with modern Python frameworks. It allows users to create and manage custom course content and generate AI-based summaries using OpenAI (GPT-4o). The summary generation runs asynchronously using **Celery + Redis**, and each user is limited to **3 AI summaries per day.

---

## ⚙️ Tech Stack

- **Python 3.11** – Main programming language
- **FastAPI** – Asynchronous API framework
- **PostgreSQL** – Relational database
- **SQLAlchemy + Alembic** – ORM & migrations
- **Pydantic** – Data validation and serialization
- **Celery** – Background task processing
- **Redis** – Celery broker and result backend
- **OpenAI (gpt-4o)** – AI summarization engine
- **Docker & Docker Compose** – Containerized setup
- **Pre-commit Hooks** – Code quality automation

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nika-alaverdashvili/fastapi-ai-course-summarizer.git
cd fastapi-ai-course-summarizer
```

### 2. Setup environment

```bash
cp .env.sample .env
```

Update your OpenAI key, database credentials, etc.

### 3. Build and run Docker services

```bash
make build
make run
```

App available at:
📎 [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

---

## 🧪 Development Commands

- Run migrations
  ```bash
  make migrate
  ```

- Generate new migration
  ```bash
  make migrations name="your_message"
  ```

- Install & update pre-commit
  ```bash
  make install_pre_commit
  ```

- Run pre-commit manually
  ```bash
  make run_pre_commit
  ```

---

## 🔐 Authentication Endpoints

| Method | Endpoint            | Description                           |
|--------|---------------------|---------------------------------------|
| POST   | `/users`            | Register a new user                   |
| POST   | `/users/login`      | Login and receive JWT tokens          |
| POST   | `/users/refresh`    | Refresh tokens                        |
| POST   | `/users/change-password` | Change user password            |
| GET    | `/users/me`         | Get current user info                 |

---

## 📚 Course Endpoints

| Method | Endpoint                           | Description                                             |
|--------|------------------------------------|---------------------------------------------------------|
| POST   | `/courses`                         | Create a new course                                     |
| GET    | `/courses`                         | Retrieve all user's courses                             |
| GET    | `/courses/{course_id}`             | Retrieve a specific course by UUID                     |
| DELETE | `/courses/{course_id}`             | Delete a course by UUID                                 |
| PATCH  | `/courses/update-summary`          | Manually update the AI-generated summary                |
| POST   | `/generate_summary`                | Generate an AI summary (rate-limited to 3/day per user) |

---

## 🧠 Summary Generation

- Triggered via `/generate_summary`
- Processed in background with Celery
- AI summary stored in `Course.ai_summary`
- Max 3 generations per user/day (in-memory throttling)

---

## 🔍 Health Check Endpoints

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| GET    | `/ping-db`     | Checks DB connection     |
| GET    | `/ping-redis`  | Checks Redis connection  |
| GET    | `/`            | App health status        |

---

## 📎 Sample JSON Payloads

### Register

```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

### Login

```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

### Create Course

```json
{
  "course_title": "Mastering Python for Data Science",
  "course_description": "This comprehensive course teaches the fundamentals of Python programming with a focus on data science applications, including NumPy, pandas, data visualization, and machine learning basics."
}
```

### Generate Summary

```json
{
  "course_id": "uuid-here",
  "new_description": "This comprehensive course teaches the fundamentals of Python programming with a focus on data science applications, including NumPy, pandas, data visualization, and machine learning basics."
}
```

### Update AI Summary

```json
{
  "course_id": "uuid-here",
  "new_summary": "This is my manual updated summary"
}
```

---

## 📁 Project Structure

```
.
├── app/
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API routes
│   ├── schemas/            # Pydantic models
│   ├── db/                 # Database configs
│   ├── tasks/              # Celery task modules
│   ├── utils/              # JWT, auth, throttle logic
│   ├── main.py             # FastAPI app instance
│   └── celery_worker.py    # Celery entrypoint
├── .env.sample             # Env config template
├── Dockerfile              # App Docker build
├── docker-compose.yaml     # Service orchestrator
├── Makefile                # CLI helper commands
├── alembic/                # DB migrations
└── README.md
```

---

## ✅ Code Quality

- **Pre-commit hooks:**
  - `black`, `isort`, `flake8`, `check-yaml`, etc.
- Run them manually with:

```bash
make run_pre_commit
```

---
