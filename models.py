from datetime import datetime, timedelta, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    paid_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def has_access(self) -> bool:
        if self.paid_until is None:
            return False
        return self.paid_until > datetime.now(timezone.utc).replace(tzinfo=None)

    def grant_three_months(self) -> None:
        self.paid_until = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=90)
