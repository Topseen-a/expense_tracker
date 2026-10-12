from datetime import timedelta

from app.exceptions.base import ValidationException
from app.exceptions.expense_exceptions import ExpenseNotFoundException, UnauthorizedExpenseAccessException
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense_schema import CreateExpenseRequest, ExpenseResponse, UpdateExpenseRequest
from app.schemas.validators import parse_iso_date


class ExpenseService:
    def __init__(self, expense_repo=None):
        self.expense_repo = expense_repo or ExpenseRepository()

    def create_expense(self, user_id: int, data):
        request = CreateExpenseRequest(data).validate()

        expense = Expense(
            amount=request.amount,
            category=request.category,
            user_id=user_id,
        )
        if request.date is not None:
            expense.date = request.date

        saved_expense = self.expense_repo.create_expense(expense)
        return ExpenseResponse(saved_expense).to_dict()

    def get_expense_by_id(self, expense_id: int, user_id: int):
        expense = self._get_owned_expense(expense_id, user_id)
        return ExpenseResponse(expense).to_dict()

    def get_user_expenses(self, user_id: int):
        expenses = self.expense_repo.get_expenses_by_user_id(user_id)
        return [ExpenseResponse(expense).to_dict() for expense in expenses]

    def update_expense(self, expense_id: int, data, user_id: int):
        request = UpdateExpenseRequest(data).validate()
        expense = self._get_owned_expense(expense_id, user_id)

        if request.amount is not None:
            expense.amount = request.amount
        if request.category is not None:
            expense.category = request.category
        if request.date is not None:
            expense.date = request.date

        updated_expense = self.expense_repo.update_expense(expense)
        return ExpenseResponse(updated_expense).to_dict()

    def delete_expense(self, expense_id: int, user_id: int):
        expense = self._get_owned_expense(expense_id, user_id)
        self.expense_repo.delete_expense(expense)
        return {"message": "Expense deleted successfully"}

    def get_expenses_by_category(self, user_id: int, category: str):
        expenses = self.expense_repo.get_expenses_by_category(user_id, category.strip())
        return [ExpenseResponse(expense).to_dict() for expense in expenses]

    def get_expenses_by_date_range(self, user_id: int, start_date_str: str, end_date_str: str):
        start_date = parse_iso_date(start_date_str)
        end_date = parse_iso_date(end_date_str)
        if start_date is None or end_date is None:
            raise ValidationException(errors={"date": "Invalid date format. Use YYYY-MM-DD"})
        if start_date > end_date:
            raise ValidationException(errors={"date": "start_date cannot be after end_date"})

        # The end date is inclusive: a bare date like 2026-10-12 covers that whole day.
        is_bare_date = len(end_date_str) == 10
        end_exclusive = end_date + (timedelta(days=1) if is_bare_date else timedelta(microseconds=1))

        expenses = self.expense_repo.get_expenses_by_date_range(user_id, start_date, end_exclusive)
        return [ExpenseResponse(expense).to_dict() for expense in expenses]

    def get_monthly_total(self, user_id: int, year: int, month: int):
        if not 1 <= month <= 12:
            raise ValidationException(errors={"month": "Month must be between 1 and 12"})

        total = self.expense_repo.get_monthly_total(user_id, year, month)
        return {
            "user_id": user_id,
            "year": year,
            "month": month,
            "total_expense": float(total),
        }

    def _get_owned_expense(self, expense_id: int, user_id: int):
        expense = self.expense_repo.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException()
        if expense.user_id != user_id:
            raise UnauthorizedExpenseAccessException()
        return expense
