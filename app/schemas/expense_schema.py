from app.exceptions.base import ValidationException
from app.schemas.validators import clean_string, parse_amount, parse_iso_date, require_json_object

CATEGORY_MAX_LENGTH = 50


def _validate_category(category, errors, required):
    if category is None:
        if required:
            errors["category"] = "Category is required"
    elif not isinstance(category, str) or not category:
        errors["category"] = "Category cannot be empty"
    elif len(category) > CATEGORY_MAX_LENGTH:
        errors["category"] = f"Category cannot exceed {CATEGORY_MAX_LENGTH} characters"


def _validate_date(raw_date, errors):
    if raw_date is None:
        return None
    parsed = parse_iso_date(raw_date)
    if parsed is None:
        errors["date"] = "Invalid date format. Use YYYY-MM-DD"
    return parsed


class CreateExpenseRequest:
    def __init__(self, data):
        data = require_json_object(data)
        self._raw_amount = data.get("amount")
        self._raw_date = data.get("date")
        self.category = clean_string(data.get("category"))
        self.amount = None
        self.date = None

    def validate(self):
        errors = {}

        if self._raw_amount is None:
            errors["amount"] = "Amount is required"
        else:
            self.amount, error = parse_amount(self._raw_amount)
            if error:
                errors["amount"] = error

        _validate_category(self.category, errors, required=True)
        self.date = _validate_date(self._raw_date, errors)

        if errors:
            raise ValidationException(errors=errors)
        return self


class UpdateExpenseRequest:
    def __init__(self, data):
        data = require_json_object(data)
        self._raw_amount = data.get("amount")
        self._raw_date = data.get("date")
        self.category = clean_string(data.get("category"))
        self.amount = None
        self.date = None

    def validate(self):
        errors = {}

        if self._raw_amount is not None:
            self.amount, error = parse_amount(self._raw_amount)
            if error:
                errors["amount"] = error

        _validate_category(self.category, errors, required=False)
        self.date = _validate_date(self._raw_date, errors)

        if errors:
            raise ValidationException(errors=errors)
        return self


class ExpenseResponse:
    def __init__(self, expense):
        if not expense:
            raise ValueError("Expense cannot be None")

        self.id = expense.id
        self.amount = float(expense.amount)
        self.category = expense.category
        self.date = expense.date.isoformat() if expense.date else None

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }
