import logging
import os

from flask import Flask, jsonify

from app.config import config_by_name
from app.exceptions.handlers import register_error_handlers
from app.extensions import db, jwt, migrate


def create_app(config_name=None):
    config_name = config_name or os.getenv("APP_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    _check_required_config(app)

    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models  # noqa: F401  (register models with SQLAlchemy/Alembic)
    from app.routes.expense_route import expense_bp
    from app.routes.user_route import user_bp

    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(expense_bp, url_prefix="/expense")
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


def _check_required_config(app):
    missing = [key for key in ("SECRET_KEY", "JWT_SECRET_KEY", "SQLALCHEMY_DATABASE_URI") if not app.config.get(key)]
    if missing:
        raise RuntimeError(f"Missing required configuration: {', '.join(missing)}. See .env.example.")
