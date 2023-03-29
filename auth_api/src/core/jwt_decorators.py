from functools import wraps
from http import HTTPStatus
from typing import List

from flask import make_response
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def roles_required(roles: List[str]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            token = get_jwt()
            if any(item in token["roles"] for item in roles):
                return fn(*args, **kwargs)
            else:
                return make_response(f"Only ${roles} are allowed access", HTTPStatus.METHOD_NOT_ALLOWED)

        return decorator

    return wrapper
