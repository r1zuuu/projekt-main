from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from ..models.task import Task
from ..models.user import User


class TaskRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self) -> Iterable[Task]:
        return self._session.query(Task).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._session.get(Task, task_id)

    def add(self, task: Task) -> Task:
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self._session.delete(task)
        self._session.commit()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self._session.get(User, user_id)

    def save(self) -> None:
        self._session.commit()
