from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.db.account_service import get_user_by_identity
from src.db.friends_service import get_all_friends, get_all_users


@jwt_required()
def user_info():
    identity = get_jwt_identity()
    current_user = get_user_by_identity(identity)
    friends = get_all_friends(current_user)

    users = get_all_users()

    output = {
        "users": [{"id": _.id, "login": _.login, "first_name": _.first_name, "last_name": _.last_name} for _ in users],
        "friends": [friend.id for friend in friends],
    }
    return jsonify(output)
