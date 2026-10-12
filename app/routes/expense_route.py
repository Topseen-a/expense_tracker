from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.exceptions.base import ValidationException
from app.routes.auth import current_user_id
from app.services.expense_service import ExpenseService

expense_bp = Blueprint("expense_bp", __name__)
expense_service = ExpenseService()


@expense_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    result = expense_service.create_expense(current_user_id(), request.get_json(silent=True))
    return jsonify(result), 201


@expense_bp.route("/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):
    result = expense_service.get_expense_by_id(expense_id, current_user_id())
    return jsonify(result), 200


@expense_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_expenses():
    result = expense_service.get_user_expenses(current_user_id())
    return jsonify(result), 200


@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    result = expense_service.update_expense(expense_id, request.get_json(silent=True), current_user_id())
    return jsonify(result), 200


@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    result = expense_service.delete_expense(expense_id, current_user_id())
    return jsonify(result), 200


@expense_bp.route("/filter/category", methods=["GET"])
@jwt_required()
def filter_by_category():
    category = request.args.get("category", "").strip()
    if not category:
        raise ValidationException("Category is required")

    result = expense_service.get_expenses_by_category(current_user_id(), category)
    return jsonify(result), 200


@expense_bp.route("/filter/date", methods=["GET"])
@jwt_required()
def filter_by_date():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if not start_date or not end_date:
        raise ValidationException("start_date and end_date are required")

    result = expense_service.get_expenses_by_date_range(current_user_id(), start_date, end_date)
    return jsonify(result), 200


@expense_bp.route("/summary/monthly", methods=["GET"])
@jwt_required()
def monthly_summary():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)
    if not year or not month:
        raise ValidationException("year and month are required")

    result = expense_service.get_monthly_total(current_user_id(), year, month)
    return jsonify(result), 200
