from typing import List

from src.db.db import db
from src.db.db_models import Roles, User, UsersRoles


def get_roles_by_user(login: str) -> List[Roles]:
    user = User.query.filter_by(login=login).first()
    roles = UsersRoles.query.filter_by(user_id=user.id).all()
    output = []
    for role in roles:
        role = Roles.query.filter_by(id=role.role_id).first()
        if role.name not in output:
            output.append(role.name)
    return output


def assign_role_to_user(user: User, role: Roles) -> None:
    new_assignment = UsersRoles(user_id=user.id, role_id=role.id)
    db.session.add(new_assignment)
    db.session.commit()


def detach_role_from_user(user: User, role: Roles) -> None:
    db.session.query(UsersRoles).filter_by(user_id=user.id, role_id=role.id).delete()
    db.session.commit()
