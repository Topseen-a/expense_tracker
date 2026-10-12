from datetime import UTC, datetime

from app.database import db


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __repr__(self):
        return f"<Expense id={self.id} amount={self.amount} category={self.category!r}>"
