"""Application factory for projektPINGUIN."""
from flask import Flask
from .config import Config
from .models import db

def create_app(config_object: type[Config] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    config_cls = config_object or Config
    app.config.from_object(config_cls())

    db.init_app(app)

    with app.app_context():
        from .models import task, user  # noqa: F401  pylint: disable=unused-import
        db.create_all()

        from .repositories.task_repository import TaskRepository
        from .services.task_service import TaskService
        from .controllers.task_controller import create_task_blueprint

        task_repository = TaskRepository(db.session)
        task_service = TaskService(task_repository)
        tasks_blueprint = create_task_blueprint(task_service)
        app.register_blueprint(tasks_blueprint, url_prefix="/tasks")

    return app
