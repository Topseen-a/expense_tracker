from flask import Blueprint, request, jsonify

from app.services.user_service import UserService
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    InvalidCredentialsException
)

user_bp = Blueprint("user_bp", __name__)
user_service = UserService()



@user_bp.route("/register", methods=["POST"])
def create_user():
    result = user_service.create_user(request.json)

    if isinstance(result, dict) and "errors" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        result = user_service.login_user(request.json)
        return jsonify(result), 200

    except InvalidCredentialsException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        result = user_service.get_user_by_id(user_id)
        return jsonify(result), 200

    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/email/<string:email>", methods=["GET"])
def get_user_by_email(email):
    try:
        result = user_service.get_user_by_email(email)
        return jsonify(result), 200

    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/", methods=["GET"])
def get_all_users():
    try:
        result = user_service.get_all_users()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        result = user_service.update_user(user_id, request.json)
        return jsonify(result), 200

    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = user_service.delete_user(user_id)
        return jsonify(result), 200

    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code