class CreateExpenseRequest:
    def __init__(self, data):
        self.amount = data.get("amount")
        self.category = data.get("category")

    def validate_create_expense_request(self):
        errors = {}

        if self.amount is None or self.amount <= 0:
            errors["amount"] = "Amount must be greater than 0"
        if not self.category:
            errors["category"] = "Category is required"

        return errors


class UpdateExpenseRequest:
    def __init__(self, data):
        self.amount = data.get("amount")
        self.category = data.get("category")

    def validate_update_expense_request(self):
        errors = {}

        if self.amount is not None and self.amount <= 0:
            errors["amount"] = "Amount must be greater than 0"
        if self.category is not None and not self.category.strip():
            errors["category"] = "Category cannot be empty"

        return errors


class ExpenseResponse:
    def __init__(self, expense):
        self.id = expense.id
        self.amount = expense.amount
        self.category = expense.category
        self.date = expense.date.isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }