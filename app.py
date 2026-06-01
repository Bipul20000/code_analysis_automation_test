"""Task Manager API — A simple Flask backend for managing tasks.

Provides endpoints to create, list, and delete tasks,
with data persisted to a JSON file.
"""

from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

TASKS_FILE = os.environ.get("TASKS_FILE", "tasks.json")


def _load_tasks():
    """Load tasks from the JSON file.

    Returns:
        list: A list of task dictionaries. Returns an empty list if the
        file does not exist or contains invalid JSON.
    """
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def _save_tasks(tasks):
    """Save tasks to the JSON file.

    Args:
        tasks (list): A list of task dictionaries to persist.

    Raises:
        IOError: If the file cannot be written.
    """
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


@app.route("/")
def index():
    """Render the main frontend page."""
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as a JSON array."""
    tasks = _load_tasks()
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task.

    Expects a JSON body with a non-empty 'title' string.

    Returns:
        201: The created task object.
        400: If the request body is missing, invalid, or title is empty.
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    title = data.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({"error": "'title' is required and must be a non-empty string"}), 400

    tasks = _load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title.strip(),
        "done": False
    }
    tasks.append(task)
    print(f"Task created: {task['title']}")
    _save_tasks(tasks)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by its ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        200: Confirmation that the task was deleted.
        404: If no task with the given ID exists.
    """
    tasks = _load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    if len(filtered) == len(tasks):
        return jsonify({"error": f"Task {task_id} not found"}), 404
    _save_tasks(filtered)
    return jsonify({"result": "deleted"})


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
