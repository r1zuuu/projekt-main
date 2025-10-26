"""Reusable authentication related decorators."""

from __future__ import annotations

from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar, cast

from flask import jsonify, session

F = TypeVar("F", bound=Callable[..., Any])


def login_required(func: F) -> F:
    """Ensure that an active user session exists before invoking ``func``."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required."}), HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    return cast(F, wrapper)
