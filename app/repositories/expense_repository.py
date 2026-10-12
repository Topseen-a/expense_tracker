from datetime import datetime

from sqlalchemy import extract, func, select

from app.database import db
from app.models.expense import Expense


class ExpenseRepository:
    def create_expense(self, expense: Expense):
        db.session.add(expense)
        db.session.commit()
        return expense

    def get_expense_by_id(self, expense_id: int):
        return db.session.get(Expense, expense_id)

    def get_expenses_by_user_id(self, user_id: int):
        query = select(Expense).where(Expense.user_id == user_id).order_by(Expense.date.desc())
        return db.session.scalars(query).all()

    def update_expense(self, expense: Expense):
        db.session.commit()
        return expense

    def delete_expense(self, expense: Expense):
        db.session.delete(expense)
        db.session.commit()

    def get_expenses_by_category(self, user_id: int, category: str):
        query = (
            select(Expense)
            .where(Expense.user_id == user_id, Expense.category == category)
            .order_by(Expense.date.desc())
        )
        return db.session.scalars(query).all()

    def get_expenses_by_date_range(self, user_id: int, start_date: datetime, end_date_exclusive: datetime):
        query = (
            select(Expense)
            .where(
                Expense.user_id == user_id,
                Expense.date >= start_date,
                Expense.date < end_date_exclusive,
            )
            .order_by(Expense.date.desc())
        )
        return db.session.scalars(query).all()

    def get_monthly_total(self, user_id: int, year: int, month: int):
        query = select(func.sum(Expense.amount)).where(
            Expense.user_id == user_id,
            extract("year", Expense.date) == year,
            extract("month", Expense.date) == month,
        )
        return db.session.scalar(query) or 0
