from http import HTTPStatus

from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.db.account_service import get_user_by_identity
from src.db.friends_service import add_friend_to_user, delete_friend_to_user, get_all_friends


@jwt_required()
def add_friend():
    identity = get_jwt_identity()
    current_user = get_user_by_identity(identity)

    friend_id = request.values.get("friend_id")
    friend_user = get_user_by_identity(friend_id)

    status = add_friend_to_user(current_user, friend_user)
    if status is False:
        return make_response("User already in friends list", HTTPStatus.BAD_REQUEST)

    return jsonify(msg=f"Friend {current_user.login} was add to user {friend_user.login} friends list")


@jwt_required()
def delete_friend():
    identity = get_jwt_identity()
    current_user = get_user_by_identity(identity)

    friend_id = request.values.get("friend_id")
    friend_user = get_user_by_identity(friend_id)

    status = delete_friend_to_user(current_user, friend_user)
    if status is False:
        return make_response("User not in friends list", HTTPStatus.BAD_REQUEST)

    return jsonify(msg=f"Friend {friend_user.login} was delete from user {friend_user.login} friends list")


@jwt_required()
def friends_list():
    identity = get_jwt_identity()
    current_user = get_user_by_identity(identity)
    friends = get_all_friends(current_user)
    output = [friend.id for friend in friends]
    return jsonify(friends=output)
