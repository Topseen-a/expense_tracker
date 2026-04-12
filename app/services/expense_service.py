from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense_schema import CreateExpenseRequest, UpdateExpenseRequest, ExpenseResponse
from app.exceptions.expense_exceptions import ExpenseNotFoundException


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

        return self.expense_repo.create_expense(expense)


    def get_expense_by_id(self, expense_id):
        expense = self.expense_repo.get_expense_by_id(expense_id)

        if not expense:
            raise ExpenseNotFoundException()

        return expense


    def get_user_expenses(self, user_id):
        return self.expense_repo.get_expenses_by_user_id(user_id)


    def get_all_expenses(self):
        expenses = self.expense_repo.get_all_expenses()

        return [
            ExpenseResponse(expense).to_dict()
            for expense in expenses
        ]


    def update_expense(self, expense_id, data):
        request = UpdateExpenseRequest(data)
        errors = request.validate_update_expense_request()

        if errors:
            return {"errors": errors}

        expense = self.expense_repo.get_expense_by_id(expense_id)

        if not expense:
            raise ExpenseNotFoundException()
        if request.amount is not None:
            expense.amount = request.amount
        if request.category is not None:
            expense.category = request.category

        self.expense_repo.update_expense()

        return expense


    def delete_expense(self, expense_id):
        expense = self.expense_repo.get_expense_by_id(expense_id)

        if not expense:
            raise ExpenseNotFoundException()

        self.expense_repo.delete_expense(expense)