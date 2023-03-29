import datetime
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from src.db.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<User {self.login}>"


def create_partition(target, connection, **kw) -> None:
    """Создает партицирование в модели LoginHistory."""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "login_history_2022" PARTITION OF "login_history" FOR VALUES FROM ('2022-1-1 00:00:00') TO ('2023-1-1 00:00:00')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "login_history_2023" PARTITION OF "login_history" FOR VALUES FROM ('2023-1-1 00:00:00') TO ('2024-1-1 00:00:00')"""
    )


class LoginHistory(db.Model):
    __tablename__ = "login_history"
    __table_args__ = (
        UniqueConstraint("id", "auth_date"),
        {
            "postgresql_partition_by": "RANGE (auth_date)",
            "listeners": [("after_create", create_partition)],
        },
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"))
    user = db.relationship(User, backref=db.backref("login_history", lazy=True))
    user_agent = db.Column(db.String(300), nullable=False)
    auth_date = db.Column(db.DateTime, nullable=False, primary_key=True, default=datetime.datetime.now())


class OAuthAccount(db.Model):
    __tablename__ = "oauth_account"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = db.relationship(User, backref=db.backref("oauth_account", lazy=True))
    social_id = db.Column(db.String(30), nullable=False)
    service_id = db.Column(db.Text, nullable=False)
    service_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<OAuthAccount {self.service_name}:{self.user_id}>"


class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<Roles {self.name}>"


class UsersRoles(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey(Roles.id))
