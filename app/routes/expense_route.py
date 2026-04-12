from flask import Blueprint, request, jsonify

from app.services.expense_service import ExpenseService
from app.exceptions.expense_exceptions import ExpenseNotFoundException

expense_bp = Blueprint("expense_bp", __name__)
expense_service = ExpenseService()


@expense_bp.route("/<int:user_id>", methods=["POST"])
def create_expense(user_id):
    result = expense_service.create_expense(user_id, request.json)

    if isinstance(result, dict) and "errors" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@expense_bp.route("/detail/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    try:
        result = expense_service.get_expense_by_id(expense_id)
        return jsonify(result), 200

    except ExpenseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@expense_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_expenses(user_id):
    result = expense_service.get_user_expenses(user_id)
    return jsonify(result), 200


@expense_bp.route("/", methods=["GET"])
def get_all_expenses():
    try:
        result = expense_service.get_all_expenses()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@expense_bp.route("/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    try:
        result = expense_service.update_expense(expense_id, request.json)
        return jsonify(result), 200

    except ExpenseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code


@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    try:
        result = expense_service.delete_expense(expense_id)
        return jsonify(result), 200

    except ExpenseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code