from app.database import db
from app.models.user import User


class UserRepository:

    def create_user(self, user: User):
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(self, user_id: int):
        return db.session.get(User, user_id)

    def get_user_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def update_user(self, user: User):
        db.session.commit()
        return user

    def delete_user(self, user: User):
        db.session.delete(user)
        db.session.commit()