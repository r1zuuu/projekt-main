from app.user.controllers.register import register_bp
from app.user.controllers.login import login_bp
from app.user.controllers.profile import profile_bp
from flask import Flask
from app import db
from app.user import register_user_blueprints

def register_user_blueprints(app):
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(profile_bp)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    register_user_blueprints(app)

    return app
