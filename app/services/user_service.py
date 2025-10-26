"""Business logic for user management."""

from __future__ import annotations

from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash

from ..models.user import User
from ..repositories.user_repository import UserRepository


class AuthenticationError(Exception):
    """Invalid credentials"""


class DuplicateUserError(Exception):
    """When duplicated username"""


class ValidationError(Exception):
    """incoming payload fails validation rules."""


@dataclass(slots=True)
class UserService:
    repository: UserRepository

    def register(self, username: str | None, password: str | None) -> User:
        username, password = self._validate_credentials(username, password)

        if self.repository.get_by_username(username):
            raise DuplicateUserError("Username is already taken.")

        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw)
        return self.repository.add(user)

    def authenticate(self, username: str | None, password: str | None) -> User:
        username, password = self._validate_credentials(username, password)

        user = self.repository.get_by_username(username)
        if not user or not check_password_hash(user.password, password):
            raise AuthenticationError("Invalid credentials.")
        return user

    def get_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValidationError("User not found.")
        return user

    @staticmethod
    def _validate_credentials(
        username: str | None,
        password: str | None,
    ) -> tuple[str, str]:
        if not username or not username.strip():
            raise ValidationError("username is required.")
        if not password or not password.strip():
            raise ValidationError("password is required.")
        if len(password) < 6:
            raise ValidationError("Password must contain at least 6 characters.")
        return username.strip(), password
