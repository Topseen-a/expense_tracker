from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.routes.auth import current_user_id
from app.services.user_service import UserService

user_bp = Blueprint("user_bp", __name__)
user_service = UserService()


@user_bp.route("/register", methods=["POST"])
def register_user():
    result = user_service.register_user(request.get_json(silent=True))
    return jsonify(result), 201


@user_bp.route("/login", methods=["POST"])
def login_user():
    result = user_service.login_user(request.get_json(silent=True))
    return jsonify(result), 200


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    result = user_service.get_user_by_id(current_user_id())
    return jsonify(result), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_user():
    result = user_service.update_user(current_user_id(), request.get_json(silent=True))
    return jsonify(result), 200


@user_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_user():
    result = user_service.delete_user(current_user_id())
    return jsonify(result), 200
