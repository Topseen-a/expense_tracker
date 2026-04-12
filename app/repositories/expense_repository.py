from app.database import db
from app.models.expense import Expense


class ExpenseRepository:

    def create_expense(self, expense: Expense):
        db.session.add(expense)
        db.session.commit()
        return expense

    def get_expense_by_id(self, expense_id: int):
        return Expense.query.get(expense_id)

    def get_expenses_by_user_id(self, user_id: int):
        return Expense.query.filter_by(user_id=user_id).all()

    def get_all_expenses(self):
        return Expense.query.all()

    def update_expense(self):
        db.session.commit()

    def delete_expense(self, expense: Expense):
        db.session.delete(expense)
        db.session.commit()