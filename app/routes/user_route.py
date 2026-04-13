from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.exceptions.user_exceptions import UserNotFoundException, EmailAlreadyExistsException, InvalidCredentialsException

user_bp = Blueprint("user_bp", __name__)
user_service = UserService()


@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        result = user_service.register_user(request.json)
        if "errors" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except EmailAlreadyExistsException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        result = user_service.login_user(request.json)
        if "errors" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except InvalidCredentialsException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        result = user_service.get_user_by_id(user_id)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_user():
    try:
        user_id = get_jwt_identity()
        result = user_service.update_user(user_id, request.json)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@user_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_user():
    try:
        user_id = get_jwt_identity()
        result = user_service.delete_user(user_id)
        return jsonify(result), 200
    except UserNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code