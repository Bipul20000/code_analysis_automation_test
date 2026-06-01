from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "done": False
    }
    tasks.append(task)
    print(f"Task created: {task['title']}")
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    tasks = [t for t in tasks if t["id"] != task_id]
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)
    return jsonify({"result": "deleted"})


if __name__ == "__main__":
    app.run(debug=True)
