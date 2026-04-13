from app.database import db
from app.models.expense import Expense
from datetime import datetime
from sqlalchemy import extract, func


class ExpenseRepository:

    def create_expense(self, expense: Expense):
        db.session.add(expense)
        db.session.commit()
        return expense

    def get_expense_by_id(self, expense_id: int):
        return db.session.get(Expense, expense_id)

    def get_expenses_by_user_id(self, user_id: int):
        return Expense.query.filter_by(user_id=user_id).all()

    def update_expense(self, expense: Expense):
        db.session.commit()
        return expense

    def delete_expense(self, expense: Expense):
        db.session.delete(expense)
        db.session.commit()

    def get_expenses_by_category(self, user_id: int, category: str):
        return Expense.query.filter_by(
            user_id=user_id,
            category=category
        ).all()

    def get_expenses_by_date_range(self, user_id: int, start_date: datetime, end_date: datetime):
        return Expense.query.filter(
            Expense.user_id == user_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).all()

    def get_monthly_total(self, user_id: int, year: int, month: int):
        total = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).scalar()

        return total or 0