import os
import json
from datetime import datetime


class Task:
    def __init__(self, id, description, status="todo", createdAt=None, updatedAt=None):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt or datetime.now().isoformat()
        self.updatedAt = updatedAt or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }


class TaskManager:
    def __init__(self):
        self.file_path = "tasks.txt"
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    tasks_data = json.load(f)
                    self.tasks = [Task(**task) for task in tasks_data]
                except json.JSONDecodeError:
                    self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.file_path, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, description):
        task_id = max((task.id for task in self.tasks), default=0) + 1
        task = Task(task_id, description)
        self.tasks.append(task)
        self.save_tasks()
        return f"Task '{description}' added successfully with ID {task_id}."

    def update_task(self, task_id, new_description):
        for task in self.tasks:
            if task.id == task_id:
                task.description = new_description
                task.updatedAt = datetime.now().isoformat()
                self.save_tasks()
                return f"Task {task_id} updated successfully."
        return f"Task {task_id} not found."

    def delete_task(self, task_id):
        task_exists = any(task.id == task_id for task in self.tasks)
        if task_exists:
            self.tasks = [task for task in self.tasks if task.id != task_id]
            self.save_tasks()
            return f"Task {task_id} deleted."
        return f"Task {task_id} does not exist."

    def mark_in_progress(self, task_id):
        return self._change_task_status(task_id, "in_progress")

    def mark_done(self, task_id):
        return self._change_task_status(task_id, "done")

    def list_tasks(self, status=None):
        filtered_tasks = self.tasks if not status else [task for task in self.tasks if task.status == status]
        if filtered_tasks:
            return "\n".join(
                [f"ID: {task.id}, Description: {task.description}, Status: {task.status}" for task in filtered_tasks])
        return "No tasks available."

    def _change_task_status(self, task_id, status):
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                task.updatedAt = datetime.now().isoformat()
                self.save_tasks()
                return f"Task {task_id} marked as {status}."
        return f"Task {task_id} not found."
