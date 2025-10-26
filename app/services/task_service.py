from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Iterable

from ..models.task import PRIORITY_ENUM, STATUS_ENUM, Task
from ..repositories.task_repository import TaskRepository


class NotFoundError(Exception):



class ValidationError(Exception):



@dataclass(slots=True)
class TaskService:


    repository: TaskRepository

    def list_tasks(self) -> Iterable[Task]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found.")
        return task

    def create_task(self, data: Dict[str, Any]) -> Task:
        user_id = data.get("user_id")
        if user_id is None:
            raise ValidationError("user_id is required.")

        if not self.repository.get_user_by_id(user_id):
            raise NotFoundError("User not found.")

        status = data.get("status", "pending")
        priority = data.get("priority", "medium")
        self._validate_status(status)
        self._validate_priority(priority)

        task = Task(
            task_name=data.get("task_name", ""),
            user_id=user_id,
            status=status,
            due_date=self._parse_date(data.get("due_date")),
            priority=priority,
        )

        if not task.task_name:
            raise ValidationError("task_name is required.")

        return self.repository.add(task)

    def update_task(self, task_id: int, data: Dict[str, Any]) -> Task:
        task = self.get_task(task_id)

        if "task_name" in data:
            new_name = data["task_name"]
            if not new_name:
                raise ValidationError("task_name cannot be empty.")
            task.task_name = new_name

        if "status" in data:
            self._validate_status(data["status"])
            task.status = data["status"]

        if "priority" in data:
            self._validate_priority(data["priority"])
            task.priority = data["priority"]

        if "due_date" in data:
            task.due_date = self._parse_date(data["due_date"])

        self.repository.save()
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.repository.delete(task)

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in STATUS_ENUM:
            raise ValidationError("Invalid status value.")

    @staticmethod
    def _validate_priority(priority: str) -> None:
        if priority not in PRIORITY_ENUM:
            raise ValidationError("Invalid priority value.")

    @staticmethod
    def _parse_date(value: Any) -> date | None:
        if value in (None, ""):
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        try:
            return date.fromisoformat(str(value))
        except (TypeError, ValueError) as exc:
            raise ValidationError("Invalid due_date format. Use ISO format (YYYY-MM-DD).") from exc
