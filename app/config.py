"""Application configuration objects."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


def _load_environment() -> None:
    """Load variables from a local ``.env`` file if it exists."""

    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


@dataclass(slots=True)
class Config:
    """Default runtime configuration."""

    SQLALCHEMY_DATABASE_URI: str = field(
        default="sqlite:///instance/app.db",
        init=False,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = field(default=False, init=False)
    JSON_SORT_KEYS: bool = field(default=False, init=False)
    SECRET_KEY: str = field(default="dev-secret", init=False)

    def __post_init__(self) -> None:  # pragma: no cover - trivial assignments
        _load_environment()
        self.SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            self.SQLALCHEMY_DATABASE_URI,
        )
        self.SECRET_KEY = os.getenv("SECRET_KEY", self.SECRET_KEY)


@dataclass(slots=True)
class TestingConfig(Config):
    """Configuration used by the automated test-suite."""

    TESTING: bool = field(default=True, init=False)
    SQLALCHEMY_DATABASE_URI: str = field(default="sqlite:///:memory:", init=False)
    PROPAGATE_EXCEPTIONS: bool = field(default=True, init=False)
