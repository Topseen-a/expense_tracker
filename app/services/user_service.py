from flask_jwt_extended import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import CreateUserRequest, LoginUserRequest, UserResponse
from app.exceptions.user_exceptions import UserNotFoundException, EmailAlreadyExistsException, InvalidCredentialsException


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()


    def register_user(self, data):
        request = CreateUserRequest(data)
        errors = request.validate_create_user_request()
        if errors:
            return {"errors": errors}

        existing_user = self.user_repo.get_user_by_email(request.email)
        if existing_user:
            raise EmailAlreadyExistsException()

        user = User(
            name=request.name,
            email=request.email,
            phone_number=request.phone_number
        )
        user.set_password(request.password)
        saved_user = self.user_repo.create_user(user)

        return UserResponse(saved_user).to_dict()


    def login_user(self, data):
        request = LoginUserRequest(data)
        errors = request.validate_login_user_request()
        if errors:
            return {"errors": errors}

        user = self.user_repo.get_user_by_email(request.email)
        if not user or not user.check_password(request.password):
            raise InvalidCredentialsException()

        access_token = create_access_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "user": UserResponse(user).to_dict()
        }


    def get_user_by_id(self, user_id):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        return UserResponse(user).to_dict()


    def get_user_by_email(self, email):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundException()

        return UserResponse(user).to_dict()



    def update_user(self, user_id, data):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        if "name" in data and data["name"]:
            user.name = data["name"]
        if "phone_number" in data and data["phone_number"]:
            user.phone_number = data["phone_number"]
        if "password" in data and data["password"]:
            user.set_password(data["password"])

        self.user_repo.update_user(user)
        return UserResponse(user).to_dict()


    def delete_user(self, user_id):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        self.user_repo.delete_user(user)
        return {"message": "User deleted successfully"}