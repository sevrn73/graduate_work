import random
import string

from src.db.account_service import create_user
from src.db.db import db
from src.db.db_models import OAuthAccount, User


def generate_password(size: int = 20) -> str:
    chars = string.ascii_letters + string.punctuation + string.digits
    return "".join(random.choice(chars) for _ in range(size))


def get_account() -> None:
    account = OAuthAccount()
    db.session.add(account)
    db.session.commit()


def add_record_to_oauth_account(user_id, social_id, service_id, service_name) -> None:
    account = OAuthAccount(user_id=user_id, social_id=social_id, service_id=service_id, service_name=service_name)
    db.session.add(account)
    db.session.commit()


def create_user_oauth(username: str, email: str, social_id: str, service_id: str, service_name: str) -> User:
    login = username
    password = generate_password()
    new_user = create_user(login, password, email)
    add_record_to_oauth_account(new_user.id, social_id, service_id, service_name)
    return new_user
