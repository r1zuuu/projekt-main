from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import Blueprint, jsonify, request, session
from werkzeug.exceptions import HTTPException

from ..services.task_service import NotFoundError, TaskService, ValidationError
from ..auth.decorators import login_required


def create_task_blueprint(task_service: TaskService) -> Blueprint:

    blueprint = Blueprint("tasks", __name__)

    @blueprint.errorhandler(NotFoundError)
    def handle_not_found(error: NotFoundError):
        return jsonify({"error": str(error)}), HTTPStatus.NOT_FOUND

    @blueprint.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST

    @blueprint.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        if isinstance(error, HTTPException):
            return error
        return (
            jsonify({"error": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @blueprint.route("/", methods=["GET"])
    def list_tasks():
        tasks = [task.to_dict() for task in task_service.list_tasks()]
        return jsonify(tasks), HTTPStatus.OK

    @blueprint.route("/", methods=["POST"])
    @login_required
    def create_task():
        payload: dict[str, Any] = request.get_json(force=True, silent=True) or {}
        payload.setdefault("user_id", session["user_id"])
        task = task_service.create_task(payload)
        return jsonify(task.to_dict()), HTTPStatus.CREATED

    @blueprint.route("/<int:task_id>", methods=["GET"])
    def get_task(task_id: int):
        task = task_service.get_task(task_id)
        return jsonify(task.to_dict()), HTTPStatus.OK

    @blueprint.route("/<int:task_id>", methods=["PUT"])
    @login_required
    def update_task(task_id: int):
        payload: dict[str, Any] = request.get_json(force=True, silent=True) or {}
        task = task_service.update_task(task_id, payload)
        return jsonify(task.to_dict()), HTTPStatus.OK

    @blueprint.route("/<int:task_id>", methods=["DELETE"])
    @login_required
    def delete_task(task_id: int):
        task_service.delete_task(task_id)
        return jsonify({"message": "Task deleted successfully."}), HTTPStatus.OK

    return blueprint
