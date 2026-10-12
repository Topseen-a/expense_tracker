from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.database import db

jwt = JWTManager()
migrate = Migrate()

__all__ = ["db", "jwt", "migrate"]
