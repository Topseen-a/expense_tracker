from datetime import datetime

from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense_schema import CreateExpenseRequest, UpdateExpenseRequest, ExpenseResponse
from app.exceptions.expense_exceptions import ExpenseNotFoundException, UnauthorizedExpenseAccessException


class ExpenseService:
    def __init__(self):
        self.expense_repo = ExpenseRepository()


    def create_expense(self, user_id, data):
        request = CreateExpenseRequest(data)
        errors = request.validate_create_expense_request()
        if errors:
            return {"errors": errors}

        expense = Expense(
            amount=request.amount,
            category=request.category,
            user_id=user_id
        )

        saved_expense = self.expense_repo.create_expense(expense)
        return ExpenseResponse(saved_expense).to_dict()


    def get_expense_by_id(self, expense_id, user_id):
        expense = self.expense_repo.get_expense_by_id(expense_id)
        if not expense:
            raise ExpenseNotFoundException()
        if expense.user_id != int(user_id):
            raise UnauthorizedExpenseAccessException()

        return ExpenseResponse(expense).to_dict()


    def get_user_expenses(self, user_id):
        expenses = self.expense_repo.get_expenses_by_user_id(user_id)
        return [
            ExpenseResponse(expense).to_dict()
            for expense in expenses
        ]


    def update_expense(self, expense_id, data, user_id):
        request = UpdateExpenseRequest(data)
        errors = request.validate_update_expense_request()
        if errors:
            return {"errors": errors}

        expense = self.expense_repo.get_expense_by_id(expense_id)

        if not expense:
            raise ExpenseNotFoundException()
        if expense.user_id != int(user_id):
            raise UnauthorizedExpenseAccessException()
        if request.amount is not None:
            expense.amount = request.amount
        if request.category is not None:
            expense.category = request.category

        updated_expense = self.expense_repo.update_expense(expense)
        return ExpenseResponse(updated_expense).to_dict()


    def delete_expense(self, expense_id, user_id):
        expense = self.expense_repo.get_expense_by_id(expense_id)

        if not expense:
            raise ExpenseNotFoundException()
        if expense.user_id != user_id:
            raise UnauthorizedExpenseAccessException()
        self.expense_repo.delete_expense(expense)

        return {"message": "Expense deleted successfully"}


    def get_expenses_by_category(self, user_id, category):
        expenses = self.expense_repo.get_expenses_by_category(user_id, category)
        return [
            ExpenseResponse(expense).to_dict()
            for expense in expenses
        ]


    def get_expenses_by_date_range(self, user_id, start_date_str, end_date_str):
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return {"errors": {"date": "Invalid date format. Use this format (YYYY-MM-DD)"}}

        expenses = self.expense_repo.get_expenses_by_date_range(user_id, start_date, end_date)
        return [
            ExpenseResponse(expense).to_dict()
            for expense in expenses
        ]


    def get_monthly_total(self, user_id, year, month):
        total = self.expense_repo.get_monthly_total(user_id, year, month)
        return {
            "user_id": user_id,
            "year": year,
            "month": month,
            "total_expense": total
        }