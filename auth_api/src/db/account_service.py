import uuid
from typing import List

from src.db.db import db
from src.db.db_models import LoginHistory, User
from werkzeug.security import generate_password_hash


def get_user_by_login(login: str) -> User:
    user = User.query.filter_by(login=login).first()

    return user


def get_user_by_identity(identity: uuid) -> User:
    user = User.query.filter_by(id=identity).first()

    return user


def add_record_to_login_history(id: uuid, user_agent: str) -> None:
    new_session = LoginHistory(user_id=id, user_agent=user_agent)
    db.session.add(new_session)
    db.session.commit()


def create_user(login: str, password: str, first_name:str, last_name:str,  email: str = None) -> User:
    hashed_password = generate_password_hash(password)
    new_user = User(login=login, password=hashed_password, email=email, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def delete_user(user_id: str) -> None:
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()


def change_login_in_db(user: User, new_login: str) -> None:
    user.login = new_login
    db.session.commit()


def change_password_in_db(user: User, new_password: str) -> None:
    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()


def get_login_hystory(identity: uuid, page: int, per_page: int) -> List:
    return (
        LoginHistory.query.filter_by(user_id=identity)
        .order_by(LoginHistory.auth_date.desc())
        .paginate(page=page, per_page=per_page)
    )
