"""Flask blueprint exposing the user REST API."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import Blueprint, jsonify, request, session
from werkzeug.exceptions import HTTPException

from ..auth.decorators import login_required
from ..services.user_service import (
    AuthenticationError,
    DuplicateUserError,
    UserService,
    ValidationError,
)


def create_user_blueprint(user_service: UserService) -> Blueprint:
    blueprint = Blueprint("users", __name__)

    @blueprint.errorhandler(AuthenticationError)
    @blueprint.errorhandler(DuplicateUserError)
    @blueprint.errorhandler(ValidationError)
    def handle_domain_error(error: Exception):
        status = HTTPStatus.BAD_REQUEST
        if isinstance(error, AuthenticationError):
            status = HTTPStatus.UNAUTHORIZED
        return jsonify({"error": str(error)}), status

    @blueprint.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        if isinstance(error, HTTPException):
            return error
        return jsonify({"error": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

    @blueprint.post("/register")
    def register_user():
        payload: dict[str, Any] = request.get_json(force=True, silent=True) or {}
        user = user_service.register(payload.get("username"), payload.get("password"))
        return jsonify(user.to_dict()), HTTPStatus.CREATED

    @blueprint.post("/login")
    def login_user():
        payload: dict[str, Any] = request.get_json(force=True, silent=True) or {}
        user = user_service.authenticate(payload.get("username"), payload.get("password"))
        session["user_id"] = user.id
        return jsonify(user.to_dict()), HTTPStatus.OK

    @blueprint.get("/logout")
    def logout_user():
        session.pop("user_id", None)
        return jsonify({"message": "Logged out."}), HTTPStatus.OK

    @blueprint.get("/profile")
    @login_required
    def profile():
        user = user_service.get_by_id(session["user_id"])
        return jsonify(user.to_dict()), HTTPStatus.OK

    return blueprint
