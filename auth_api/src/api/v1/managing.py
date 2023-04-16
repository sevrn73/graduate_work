from http import HTTPStatus

from flask import jsonify, make_response, request
from src.core.jwt_decorators import roles_required
from src.db.account_service import get_user_by_login
from src.db.managing_service import assign_role_to_user, detach_role_from_user, get_roles_by_user
from src.db.roles_service import get_role_by_name


@roles_required(["admin", "manager"])
def user_roles():
    login = request.values.get("login", None)
    if not login:
        return make_response("Login is empty", HTTPStatus.UNAUTHORIZED)
    users_roles = get_roles_by_user(login)
    return jsonify(roles=users_roles)


@roles_required(["admin", "manager"])
def assign_role():
    result = get_user_and_role()
    if isinstance(result, tuple):
        login, role, db_role, user_db = result
    else:
        return result
    assign_role_to_user(user_db, db_role)
    return jsonify(msg=f"Role {role} was assigned to user {login}")


@roles_required(["admin", "manager"])
def detach_role():
    result = get_user_and_role()
    if isinstance(result, tuple):
        login, role, db_role, user_db = result
    else:
        return result
    detach_role_from_user(user_db, db_role)
    return jsonify(msg=f"Role {role} was  detached from user {login}")


def get_user_and_role():
    login = request.values.get("login", None)
    role = request.values.get("role", None)
    if not role or not login:
        return make_response("Role or login is empty", HTTPStatus.UNAUTHORIZED)
    db_role = get_role_by_name(role)
    if not db_role:
        return make_response("Role does not exist", HTTPStatus.CONFLICT)
    user_db = get_user_by_login(login)
    if not user_db:
        return make_response("User does not exist", HTTPStatus.CONFLICT)

    return login, role, db_role, user_db
