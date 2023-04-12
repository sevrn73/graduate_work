from src.db.db import db
from src.db.db_models import User


def add_friend_to_user(user: User, friend: str) -> bool:
    status = user.befriend(friend)
    db.session.commit()
    return status


def delete_friend_to_user(user: User, friend: str) -> bool:
    status = user.unfriend(friend)
    db.session.commit()
    return status


def get_all_friends(user: User) -> list:
    user_friends = user.friends
    return user_friends
