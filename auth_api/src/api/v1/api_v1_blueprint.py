from flask import Blueprint
from src.api.v1.account import (
    change_login,
    change_password,
    check_perm,
    delete,
    login,
    login_history,
    logout,
    refresh,
    sign_up,
)
from src.api.v1.friends import add_friend, delete_friend, friends_list
from src.api.v1.managing import assign_role, detach_role, user_roles
from src.api.v1.roles import change_role, create_role, delete_role, roles_list
from src.api.v1.user_info import user_info

app_v1_blueprint = Blueprint("v1", __name__)
app_v1_blueprint.add_url_rule("/check_perm", methods=["GET"], view_func=check_perm)
app_v1_blueprint.add_url_rule("/delete_user", methods=["POST"], view_func=delete)
app_v1_blueprint.add_url_rule("/change_login", methods=["POST"], view_func=change_login)
app_v1_blueprint.add_url_rule("/change_password", methods=["POST"], view_func=change_password)
app_v1_blueprint.add_url_rule("/login", methods=["POST"], view_func=login)
app_v1_blueprint.add_url_rule("/login_history", methods=["GET"], view_func=login_history)
app_v1_blueprint.add_url_rule("/logout", methods=["DELETE"], view_func=logout)
app_v1_blueprint.add_url_rule("/refresh", methods=["GET"], view_func=refresh)
app_v1_blueprint.add_url_rule("/sign_up", methods=["POST"], view_func=sign_up)

app_v1_blueprint.add_url_rule("/create_role", methods=["POST"], view_func=create_role)
app_v1_blueprint.add_url_rule("/delete_role", methods=["DELETE"], view_func=delete_role)
app_v1_blueprint.add_url_rule("/change_role", methods=["PUT"], view_func=change_role)
app_v1_blueprint.add_url_rule("/roles_list", methods=["GET"], view_func=roles_list)

app_v1_blueprint.add_url_rule("/user_roles", methods=["GET"], view_func=user_roles)
app_v1_blueprint.add_url_rule("/assign_role", methods=["POST"], view_func=assign_role)
app_v1_blueprint.add_url_rule("/detach_role", methods=["DELETE"], view_func=detach_role)

app_v1_blueprint.add_url_rule("/add_friend", methods=["POST"], view_func=add_friend)
app_v1_blueprint.add_url_rule("/delete_friend", methods=["DELETE"], view_func=delete_friend)
app_v1_blueprint.add_url_rule("/friends_list", methods=["GET"], view_func=friends_list)

app_v1_blueprint.add_url_rule("/user_info", methods=["GET"], view_func=user_info)
