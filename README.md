# Expense Tracker API

A REST API for tracking personal expenses, built with Flask, SQLAlchemy and JWT authentication.

## Tech stack

- **Flask 3** with blueprints and an application factory
- **SQLAlchemy 2 / Flask-SQLAlchemy** with **MySQL** (PyMySQL driver)
- **Flask-Migrate (Alembic)** for schema migrations
- **Flask-JWT-Extended** for authentication
- **pytest** for tests, **ruff** for linting and formatting

## Project structure

```
app/
├── __init__.py          # Application factory (create_app)
├── config.py            # Development / Testing / Production config, loaded from env
├── extensions.py        # db, jwt, migrate instances
├── models/              # SQLAlchemy models
├── schemas/             # Request validation and response serialization
├── repositories/        # Database access
├── services/            # Business logic
├── routes/              # HTTP endpoints (blueprints)
└── exceptions/          # Domain exceptions + centralized JSON error handlers
migrations/              # Alembic migration scripts
tests/                   # pytest suite (runs against in-memory SQLite)
main.py                  # Entry point
```

A request flows through **route → service → repository → model**. Services raise exceptions such as
`ExpenseNotFoundException` or `ValidationException`, and `app/exceptions/handlers.py` turns them into JSON responses.

## Getting started

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements-dev.txt

# 3. Configure environment
cp .env.example .env        # then edit .env with your DB credentials and secrets

# 4. Create the database and apply migrations
mysql -u root -p -e "CREATE DATABASE expense_db"
flask db upgrade

# 5. Run the server
flask run
```

The API runs at `http://127.0.0.1:5000`.

### Environment variables

| Variable | Description |
|---|---|
| `APP_ENV` | `development`, `testing` or `production` (default `development`) |
| `SECRET_KEY` | Flask secret key |
| `JWT_SECRET_KEY` | Key used to sign JWTs |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | Token lifetime (default `60`) |
| `DATABASE_URL` | SQLAlchemy URL, e.g. `mysql+pymysql://user:pass@localhost/expense_db` |

The app refuses to start if `SECRET_KEY`, `JWT_SECRET_KEY` or `DATABASE_URL` is missing.

### Changing the schema

```bash
flask db migrate -m "describe the change"   # generate a migration from model changes
flask db upgrade                            # apply it
```

## Running tests and linting

```bash
pytest
ruff check .
ruff format .
```

## API reference

All endpoints except `/user/register`, `/user/login` and `/health` need an
`Authorization: Bearer <access_token>` header.

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/user/register` | Register (`name`, `email`, `phone_number`, `password`) |
| POST | `/user/login` | Log in (`email`, `password`) and get an `access_token` |
| GET | `/user/me` | Get the current user |
| PUT | `/user/me` | Update `name`, `phone_number` and/or `password` |
| DELETE | `/user/me` | Delete the current user and their expenses |

### Expenses

| Method | Endpoint | Description |
|---|---|---|
| POST | `/expense/` | Create (`amount`, `category`, optional `date` as `YYYY-MM-DD`) |
| GET | `/expense/` | List your expenses (newest first) |
| GET | `/expense/<id>` | Get one expense |
| PUT | `/expense/<id>` | Update `amount`, `category` and/or `date` |
| DELETE | `/expense/<id>` | Delete an expense |
| GET | `/expense/filter/category?category=Food` | Filter by category |
| GET | `/expense/filter/date?start_date=2026-01-01&end_date=2026-01-31` | Filter by date range (inclusive) |
| GET | `/expense/summary/monthly?year=2026&month=1` | Monthly total |

### Health

`GET /health` returns `{"status": "ok"}`.

### Error format

Every error response is JSON:

```json
{ "error": "Validation failed", "errors": { "amount": "Amount must be greater than 0" } }
```

| Status | Meaning |
|---|---|
| 400 | Invalid input |
| 401 | Missing, invalid or expired token, or wrong credentials |
| 403 | Accessing another user's expense |
| 404 | Resource not found |
| 409 | Email already registered |
| 500 | Unexpected server error |
