from app.exceptions.base import AppException


class ExpenseNotFoundException(AppException):
    status_code = 404
    message = "Expense not found"


class UnauthorizedExpenseAccessException(AppException):
    status_code = 403
    message = "You cannot access this expense"
