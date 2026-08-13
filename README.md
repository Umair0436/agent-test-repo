# Mini Task Tracker

A deliberately small task list app — frontend, backend, and a database layer —
built as a real test target for an AI Repo Agent workflow, not as a real product.

## Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:5000`. Endpoints:

- `GET /api/tasks`
- `POST /api/tasks` — `{"title": "..."}`
- `DELETE /api/tasks/<id>`
- `PATCH /api/tasks/<id>/toggle`

Tests: `cd backend && pytest`

## Frontend

Open `frontend/index.html` directly in a browser (or serve the folder with
any static file server). Talks to the backend at `http://localhost:5000`.

## Database

SQLite, schema in `backend/schema.sql`. The database file
(`backend/tasks.db`) is created automatically on first run and is not
committed to the repo.
