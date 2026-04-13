from flask import Flask
from app.database import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    db.init_app(app)
    jwt = JWTManager(app)

    from app.routes.user_route import user_bp
    from app.routes.expense_route import expense_bp

    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(expense_bp, url_prefix="/expenses")

    return app