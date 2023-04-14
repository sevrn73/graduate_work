from http import HTTPStatus

from flask import jsonify, make_response, request

from src.core.jwt_decorators import roles_required
from src.db.roles_service import change_role_db, create_role_db, delete_role_db, get_all_roles, get_role_by_name


@roles_required(["admin"])
def create_role():
    role = request.values.get("new_role", None)
    if not role:
        return make_response("New role is empty", HTTPStatus.UNAUTHORIZED)

    create_role_db(role)
    return jsonify(msg=f"Role {role} was successfully created")


@roles_required(["admin"])
def delete_role():
    role = request.values.get("role", None)
    if not role:
        return make_response("Role is empty", HTTPStatus.UNAUTHORIZED)
    db_role = get_role_by_name(role)
    if not db_role:
        return make_response("Role does not exist", HTTPStatus.CONFLICT)
    delete_role_db(db_role)
    return jsonify(msg=f"Role {role} was successfully deleted")


@roles_required(["admin"])
def change_role():
    role = request.values.get("role", None)
    new_role = request.values.get("new_name", None)
    if not role or not new_role:
        return make_response("Role or new name is empty", HTTPStatus.UNAUTHORIZED)

    change_role_db(role, new_role)
    return jsonify(msg=f"Role {role} was successfully changed")


@roles_required(["admin"])
def roles_list():
    roles = get_all_roles()
    output = [role.name for role in roles]
    return jsonify(roles=output)
