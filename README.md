# Library Management System

AngularJS 1.8 frontend · Flask REST API · SQLAlchemy · SQLite · Docker Compose

## Run everything

```bash
docker compose up --build
```

| Service  | URL                          |
| -------- | ---------------------------- |
| Frontend | http://localhost:8080        |
| API      | http://localhost:5000/api/books |

The database (`instance/library.db`) lives in a Docker volume and is seeded
with 10 sample books on first start (set `AUTO_SEED=0` to disable).
Stop with `docker compose down` (add `-v` to also wipe the data).

## Run without Docker

```bash
# backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py                 # http://localhost:5000 (creates tables + seeds)

# frontend - any static server that proxies /api to :5000, e.g. via Docker:
docker compose up --build frontend
```

## Tests

```bash
cd backend
pytest
```

Tests use an isolated in-memory SQLite database (28 tests).

## API

| Method | Endpoint                  | Success | Errors        |
| ------ | ------------------------- | ------- | ------------- |
| GET    | `/api/books?search=&category=` | 200 |               |
| GET    | `/api/books/categories`   | 200     |               |
| POST   | `/api/books`              | 201     | 400           |
| GET    | `/api/books/:id`          | 200     | 404           |
| PUT    | `/api/books/:id`          | 200     | 400, 404      |
| DELETE | `/api/books/:id`          | 204     | 404, 409 (borrowed) |
| POST   | `/api/books/:id/borrow`   | 200     | 400, 404, 409 |
| POST   | `/api/books/:id/return`   | 200     | 404, 409      |

Every response, including errors, is JSON: `{"error": "Book is already borrowed"}`.

## Architecture

Routes (HTTP) → `BookService` (business rules) → SQLAlchemy → SQLite.
Validation lives in `validators/`, errors are mapped centrally in `errors/handlers.py`
(400 / 404 / 409 / 500, plus JSON 404/405 for unknown routes).
A DB `CHECK` constraint guarantees `is_borrowed` and `borrower_name` stay consistent.

Frontend: `ngRoute` routes → controllers → `BookService` (the only HTTP layer).
Bootstrap 5 + custom flat theme, `ngAnimate` transitions, skeleton loaders, toasts.
All frontend libraries are vendored in `frontend/vendor` (no CDN needed).
