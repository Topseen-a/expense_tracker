import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.exceptions.base import AppException
from app.extensions import jwt

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        logger.exception("Unhandled exception")
        return jsonify({"error": "Internal server error"}), 500


@jwt.unauthorized_loader
def missing_token(reason):
    return jsonify({"error": "Authorization token is missing"}), 401


@jwt.invalid_token_loader
def invalid_token(reason):
    return jsonify({"error": "Invalid authorization token"}), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({"error": "Authorization token has expired"}), 401
