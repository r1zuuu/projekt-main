"""Pytest fixtures for the projekt application."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from app.config import TestingConfig
from app.models import db


@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):  # type: ignore[override]
    return app.test_client()
