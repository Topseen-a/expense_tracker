from flask_jwt_extended import create_access_token

from app.exceptions.user_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFoundException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserRequest, LoginUserRequest, UpdateUserRequest, UserResponse


class UserService:
    def __init__(self, user_repo=None):
        self.user_repo = user_repo or UserRepository()

    def register_user(self, data):
        request = CreateUserRequest(data).validate()

        if self.user_repo.get_user_by_email(request.email):
            raise EmailAlreadyExistsException()

        user = User(
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
        )
        user.set_password(request.password)
        saved_user = self.user_repo.create_user(user)

        return UserResponse(saved_user).to_dict()

    def login_user(self, data):
        request = LoginUserRequest(data).validate()

        user = self.user_repo.get_user_by_email(request.email)
        if not user or not user.check_password(request.password):
            raise InvalidCredentialsException()

        access_token = create_access_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "user": UserResponse(user).to_dict(),
        }

    def get_user_by_id(self, user_id: int):
        return UserResponse(self._get_user(user_id)).to_dict()

    def get_user_by_email(self, email: str):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundException()

        return UserResponse(user).to_dict()

    def update_user(self, user_id: int, data):
        request = UpdateUserRequest(data).validate()
        user = self._get_user(user_id)

        if request.name is not None:
            user.name = request.name
        if request.phone_number is not None:
            user.phone_number = request.phone_number
        if request.password is not None:
            user.set_password(request.password)

        self.user_repo.update_user(user)
        return UserResponse(user).to_dict()

    def delete_user(self, user_id: int):
        user = self._get_user(user_id)
        self.user_repo.delete_user(user)
        return {"message": "User deleted successfully"}

    def _get_user(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
