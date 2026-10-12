import re

from app.exceptions.base import ValidationException
from app.schemas.validators import clean_string, require_json_object

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_MAX_LENGTH = 50
EMAIL_MAX_LENGTH = 100
PASSWORD_MIN_LENGTH = 6


def _validate_name(name, errors, required):
    if name is None:
        if required:
            errors["name"] = "Name is required"
    elif not isinstance(name, str) or not name:
        errors["name"] = "Name cannot be empty"
    elif len(name) > NAME_MAX_LENGTH:
        errors["name"] = f"Name cannot exceed {NAME_MAX_LENGTH} characters"


def _validate_phone_number(phone_number, errors, required):
    if phone_number is None:
        if required:
            errors["phone_number"] = "Phone number is required"
    elif not isinstance(phone_number, str) or not phone_number.isdigit() or len(phone_number) != 11:
        errors["phone_number"] = "Phone number must be 11 digits"


def _validate_password(password, errors, required):
    if password is None:
        if required:
            errors["password"] = "Password is required"
    elif not isinstance(password, str) or len(password) < PASSWORD_MIN_LENGTH:
        errors["password"] = f"Password must be at least {PASSWORD_MIN_LENGTH} characters"


class CreateUserRequest:
    def __init__(self, data):
        data = require_json_object(data)
        self.name = clean_string(data.get("name"))
        email = clean_string(data.get("email"))
        self.email = email.lower() if isinstance(email, str) else email
        self.phone_number = clean_string(data.get("phone_number"))
        self.password = data.get("password")

    def validate(self):
        errors = {}

        _validate_name(self.name, errors, required=True)
        if not self.email:
            errors["email"] = "Email is required"
        elif not isinstance(self.email, str) or not EMAIL_PATTERN.match(self.email):
            errors["email"] = "Invalid email format"
        elif len(self.email) > EMAIL_MAX_LENGTH:
            errors["email"] = f"Email cannot exceed {EMAIL_MAX_LENGTH} characters"
        _validate_phone_number(self.phone_number, errors, required=True)
        _validate_password(self.password, errors, required=True)

        if errors:
            raise ValidationException(errors=errors)
        return self


class LoginUserRequest:
    def __init__(self, data):
        data = require_json_object(data)
        email = clean_string(data.get("email"))
        self.email = email.lower() if isinstance(email, str) else email
        self.password = data.get("password")

    def validate(self):
        errors = {}

        if not self.email or not isinstance(self.email, str):
            errors["email"] = "Email is required"
        if not self.password or not isinstance(self.password, str):
            errors["password"] = "Password is required"

        if errors:
            raise ValidationException(errors=errors)
        return self


class UpdateUserRequest:
    def __init__(self, data):
        data = require_json_object(data)
        self.name = clean_string(data.get("name"))
        self.phone_number = clean_string(data.get("phone_number"))
        self.password = data.get("password")

    def validate(self):
        errors = {}

        _validate_name(self.name, errors, required=False)
        _validate_phone_number(self.phone_number, errors, required=False)
        _validate_password(self.password, errors, required=False)

        if errors:
            raise ValidationException(errors=errors)
        return self


class UserResponse:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number
        self.created_at = user.created_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
