from app.database import db
from app.models.user import User


class UserRepository:

    def create_user(self, user: User):
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(self, user_id: int):
        return User.query.get(user_id)

    def get_user_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def get_all_users(self):
        return User.query.all()

    def update_user(self):
        db.session.commit()

    def delete_user(self, user: User):
        db.session.delete(user)
        db.session.commit()