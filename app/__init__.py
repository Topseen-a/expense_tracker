from flask import Flask
from app.database import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.user_route import user_bp
    from app.routes.expense_route import expense_bp

    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")

    return app