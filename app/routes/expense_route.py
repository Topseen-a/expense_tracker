from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.expense_service import ExpenseService
from app.exceptions.expense_exceptions import ExpenseNotFoundException, UnauthorizedExpenseAccessException


expense_bp = Blueprint("expense_bp", __name__)
expense_service = ExpenseService()


@expense_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()

    result = expense_service.create_expense(user_id, request.json)
    if "errors" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@expense_bp.route("/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):
    user_id = get_jwt_identity()

    try:
        result = expense_service.get_expense_by_id(expense_id, user_id)
        return jsonify(result), 200
    except ExpenseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except UnauthorizedExpenseAccessException as e:
        return jsonify({"error": e.message}), e.status_code


@expense_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_expenses():
    user_id = get_jwt_identity()
    result = expense_service.get_user_expenses(user_id)
    return jsonify(result), 200


@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()

    try:
        result = expense_service.update_expense(expense_id, request.json, user_id)
        return jsonify(result), 200
    except ExpenseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except UnauthorizedExpenseAccessException as e:
        return jsonify({"error": e.message}), e.status_code


@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()

    try:
        result = expense_service.delete_expense(expense_id, user_id)
        return jsonify(result), 200
    except ExpenseNotFoundException as e:
        return jsonify({"error": e.message}), e.status_code
    except UnauthorizedExpenseAccessException as e:
        return jsonify({"error": e.message}), e.status_code


@expense_bp.route("/filter/category", methods=["GET"])
@jwt_required()
def filter_by_category():
    user_id = get_jwt_identity()
    category = request.args.get("category")

    if not category:
        return jsonify({"error": "Category is required"}), 400

    result = expense_service.get_expenses_by_category(user_id, category)
    return jsonify(result), 200


@expense_bp.route("/filter/date", methods=["GET"])
@jwt_required()
def filter_by_date():
    user_id = get_jwt_identity()

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    result = expense_service.get_expenses_by_date_range(
        user_id, start_date, end_date
    )

    return jsonify(result), 200


@expense_bp.route("/summary/monthly", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = get_jwt_identity()

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if not year or not month:
        return jsonify({"error": "year and month are required"}), 400

    result = expense_service.get_monthly_total(user_id, year, month)
    return jsonify(result), 200