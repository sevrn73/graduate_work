import uuid
from typing import List

from src.db.db import db
from src.db.db_models import Roles, UsersRoles


def get_all_roles() -> List[Roles]:
    return Roles.query.all()


def get_role_by_name(role: str) -> Roles:
    return Roles.query.filter_by(name=role).first()


def create_role_db(role_name: str) -> None:
    new_role = Roles(name=role_name)
    db.session.add(new_role)
    db.session.commit()


def get_user_primary_role(user_id: uuid) -> Roles:
    users_roles = UsersRoles.query.filter_by(user_id=user_id).all()
    if not users_roles:
        return {"roles": []}
    output = []
    for role in users_roles:
        role = Roles.query.filter_by(id=role.role_id).first()
        output.append(role.name)
    return {"roles": output}


def delete_role_db(role: Roles) -> None:
    db.session.delete(role)
    db.session.commit()


def change_role_db(role_name: str, new_name: str) -> None:
    role = Roles.query.filter_by(name=role_name).first()
    role.name = new_name
    db.session.commit()
