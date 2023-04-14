from http import HTTPStatus

from flask import jsonify, make_response, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)


from src.db.account_service import get_user_by_identity
from src.db.friends_service import add_friend_to_user, get_all_friends, delete_friend_to_user


@jwt_required()
def user_info():
    user_id = request.args.get('user_id')
    user = get_user_by_identity(user_id)
    friends = get_all_friends(user)
    friends_list = [friend.id for friend in friends]
    output = {
        "id":user_id,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "friends_list":friends_list
    }
    return jsonify(output)