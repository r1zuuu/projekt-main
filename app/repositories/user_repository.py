
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from ..models.user import User


class UserRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        return self._session.query(User).filter_by(username=username).one_or_none()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._session.get(User, user_id)

    def save(self) -> None:
        self._session.commit()
