"""Mini Task Tracker backend -- a small Flask + SQLite API."""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

DB_PATH = Path(__file__).parent / "tasks.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    schema = (Path(__file__).parent / "schema.sql").read_text(encoding="utf-8")
    conn = get_db()
    conn.executescript(schema)
    conn.close()


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    conn = get_db()
    rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    title = (request.get_json() or {}).get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    conn = get_db()
    cursor = conn.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": task_id, "title": title, "done": 0}), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.close()
    return jsonify({"deleted": task_id})


@app.route("/api/tasks/<int:task_id>/toggle", methods=["PATCH"])
def toggle_task(task_id):
    conn = get_db()
    conn.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (1,))
    conn.commit()
    row = conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return (jsonify(dict(row)), 200) if row else (jsonify({"error": "not found"}), 404)


if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db()
    app.run(debug=True, port=5000)
