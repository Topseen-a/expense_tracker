from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from app.exceptions.base import ValidationException


def require_json_object(data):
    if not isinstance(data, dict):
        raise ValidationException("Request body must be a JSON object")
    return data


def clean_string(value):
    return value.strip() if isinstance(value, str) else value


def parse_amount(value):
    """Return (Decimal, None) on success or (None, error_message)."""
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return None, "Amount must be a number"
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        return None, "Amount must be a number"
    if not amount.is_finite():
        return None, "Amount must be a number"
    if amount <= 0:
        return None, "Amount must be greater than 0"
    if amount.as_tuple().exponent < -2:
        return None, "Amount cannot have more than 2 decimal places"
    if amount >= Decimal("10000000000"):
        return None, "Amount is too large"
    return amount, None


def parse_iso_date(value):
    """Parse 'YYYY-MM-DD' or a full ISO-8601 datetime. Returns a datetime or None."""
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.combine(date.fromisoformat(value), datetime.min.time())
        except ValueError:
            return None
