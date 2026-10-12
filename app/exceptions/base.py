class AppException(Exception):
    status_code = 500
    message = "An unexpected error occurred"

    def __init__(self, message=None, errors=None):
        self.message = message or self.message
        self.errors = errors
        super().__init__(self.message)

    def to_dict(self):
        body = {"error": self.message}
        if self.errors:
            body["errors"] = self.errors
        return body


class ValidationException(AppException):
    status_code = 400
    message = "Validation failed"
