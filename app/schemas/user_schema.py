class CreateUserRequest:
    def __init__(self, data):
        self.name = data.get("name")
        self.email = data.get("email")
        self.phone_number = data.get("phone_number")
        self.password = data.get("password")

    def validate_create_user_request(self):
        errors = {}

        if not self.name:
            errors["name"] = "Name is required"
        if not self.email:
            errors["email"] = "Email is required"
        if not self.phone_number or len(self.phone_number) != 11:
            errors["phone_number"] = "Phone number must be 11 digits"
        if not self.password or len(self.password) < 4:
            errors["password"] = "Password must be at least 4 characters"

        return errors


class LoginUserRequest:
    def __init__(self, data):
        self.email = data.get("email")
        self.password = data.get("password")

    def validate_login_user_request(self):
        errors = {}

        if not self.email:
            errors["email"] = "Email is required"
        if not self.password:
            errors["password"] = "Password is required"

        return errors


class UserResponse:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.phone_number = user.phone_number

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number
        }