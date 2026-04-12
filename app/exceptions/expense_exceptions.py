class ExpenseNotFoundException(Exception):
    def __init__(self, message="Expense not found"):
        self.message = message
        self.status_code = 404
        super().__init__(message)


class UnauthorizedExpenseAccessException(Exception):
    def __init__(self, message="You cannot access this expense"):
        self.message = message
        self.status_code = 403
        super().__init__(message)