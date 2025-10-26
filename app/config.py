from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Config:
    def __post_init__(self) -> None:
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(env_path, override=False)

        self.SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "postgresql://user:password@localhost:5432/todo_db",
        )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.JSON_SORT_KEYS = False
