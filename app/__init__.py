from flask import Flask
from .config import Config
from .models import db

def create_app(config_object: type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    config_cls = config_object or Config
    app.config.from_object(config_cls())

    db.init_app(app)

    with app.app_context():
        from .models import task, user
        db.create_all()

        from .repositories.task_repository import TaskRepository
        from .repositories.user_repository import UserRepository
        from .services.task_service import TaskService
        from .services.user_service import UserService
        from .controllers.task_controller import create_task_blueprint
        from .controllers.user_controller import create_user_blueprint

        user_repository = UserRepository(db.session)
        user_service = UserService(user_repository)

        task_repository = TaskRepository(db.session)
        task_service = TaskService(task_repository, user_repository)

        tasks_blueprint = create_task_blueprint(task_service)
        users_blueprint = create_user_blueprint(user_service)
        app.register_blueprint(tasks_blueprint, url_prefix="/tasks")
        app.register_blueprint(users_blueprint, url_prefix="/users")

    return app
