from http import HTTPStatus

from flask import jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash

from src.cache.redis_cache import redis_cache
from src.core.config import redis_settings
from src.db.account_service import (
    add_record_to_login_history,
    change_login_in_db,
    change_password_in_db,
    create_user,
    delete_user,
    get_login_hystory,
    get_user_by_identity,
    get_user_by_login,
)


def get_unauthorized_response():
    return make_response(
        "Could not verify", HTTPStatus.UNAUTHORIZED, {"WWW-Authenticate": 'Basic realm="Login required!"'}
    )


@jwt_required()
def check_perm():
    return jsonify(message="Ok")


def login():
    auth = request.authorization

    if not auth.username or not auth.password:
        return get_unauthorized_response()

    user_model = get_user_by_login(auth.username)
    if not user_model:
        return get_unauthorized_response()

    if check_password_hash(user_model.password, auth.password):
        user_agent = request.headers["user_agent"]

        add_record_to_login_history(user_model.id, user_agent)

        additional_claims = {"first_name": user_model.first_name, "last_name": user_model.last_name}

        access_token = create_access_token(identity=user_model.id, additional_claims=additional_claims, fresh=True)
        refresh_token = create_refresh_token(identity=user_model.id, additional_claims=additional_claims,)

        refresh_key = ":".join(("refresh", user_agent, str(user_model.id)))
        redis_cache._put_token(refresh_key, get_jti(refresh_token), redis_settings.REFRESH_EXPIRES_IN_SECONDS)

        return jsonify(access_token=access_token, refresh_token=refresh_token)

    return get_unauthorized_response()


@jwt_required()
def delete():
    identity = get_jwt_identity()
    delete_user(identity)

    return jsonify(msg="User successfully delete")


@jwt_required()
def change_login():
    new_login = request.values.get("new_login")
    user_model = get_user_by_login(new_login)
    if user_model:
        return make_response("Login already existed", HTTPStatus.BAD_REQUEST)

    identity = get_jwt_identity()
    current_user = get_user_by_identity(identity)
    change_login_in_db(user=current_user, new_login=new_login)

    return jsonify(msg="Login successfully changed")


@jwt_required()
def change_password():
    new_password = request.values.get("new_password")
    if not new_password:
        return make_response("Could not change password", HTTPStatus.BAD_REQUEST)

    identity = get_jwt_identity()
    current_user = get_user_by_identity(identity)
    change_password_in_db(current_user, new_password)

    return jsonify(msg="Password successfully changed")


@jwt_required()
def login_history():
    page = int(request.values.get("page"))
    per_page = int(request.values.get("per_page"))
    identity = get_jwt_identity()

    history = [
        {"user_agent": _.user_agent, "auth_date": _.auth_date}
        for _ in get_login_hystory(identity, page, per_page).items
    ]
    return jsonify(login_history=history)


@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]

    redis_cache._put_token(jti, "revoked", redis_settings.ACCESS_EXPIRES_IN_SECONDS)

    return jsonify(msg=f"{ttype.capitalize()} successfully revoked")


@jwt_required(refresh=True)
def refresh():
    user_agent = request.headers["user_agent"]

    identity = get_jwt_identity()
    token = get_jwt()
    jti = token["jti"]

    key = ":".join(("refresh", user_agent, identity))
    cache_token_jti = redis_cache._get(key)

    additional_claims = {"first_name": token["first_name"], "last_name": token["last_name"]}

    if jti == cache_token_jti:
        access_token = create_access_token(identity=identity, additional_claims=additional_claims, fresh=True)
        refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims,)

        refresh_key = ":".join(("refresh", user_agent, identity))
        redis_cache._put_token(refresh_key, get_jti(refresh_token), redis_settings.REFRESH_EXPIRES_IN_SECONDS)

        return jsonify(access_token=access_token, refresh_token=refresh_token)

    return make_response(
        "Could not verify token", HTTPStatus.UNAUTHORIZED, {"WWW-Authenticate": 'Basic realm="Login required!"'}
    )


def sign_up():
    login = request.values.get("login", None)
    password = request.values.get("password", None)
    first_name = request.values.get("first_name", None)
    last_name = request.values.get("last_name", None)
    if not login or not password:
        return make_response(
            "Login and password required",
            HTTPStatus.UNAUTHORIZED,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    user_model = get_user_by_login(login)
    if user_model:
        return make_response("Login already existed", HTTPStatus.BAD_REQUEST)

    new_user = create_user(login, password, first_name, last_name)

    additional_claims = {"first_name": first_name, "last_name": last_name}

    access_token = create_access_token(identity=new_user.id, additional_claims=additional_claims, fresh=True)
    refresh_token = create_refresh_token(identity=new_user.id, additional_claims=additional_claims)
    user_agent = request.headers["user_agent"]

    add_record_to_login_history(new_user.id, user_agent)

    refresh_key = ":".join(("refresh", user_agent, str(new_user.id)))
    redis_cache._put_token(refresh_key, get_jti(refresh_token), redis_settings.REFRESH_EXPIRES_IN_SECONDS)

    return jsonify(access_token=access_token, refresh_token=refresh_token)
