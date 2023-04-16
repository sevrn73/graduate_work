import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.db.db import SQLALCHEMY_DATABASE_URI
from src.db.db_models import Roles, User, UsersRoles
from werkzeug.security import generate_password_hash


@click.command(name="create_admin_role")
@click.argument("login", envvar="SUPERUSER_LOGIN")
@click.argument("password", envvar="SUPERUSER_PASS")
@with_appcontext
def create_admin_role(login, password):
    engine = create_engine(SQLALCHEMY_DATABASE_URI, isolation_level="REPEATABLE READ", echo=True)
    with Session(engine) as session:
        admin_user = session.query(User).filter(User.login == login).first()
        if not admin_user:
            hashed_password = generate_password_hash(password)
            admin_user = User(login=login, password=hashed_password)
            session.add(admin_user)
            session.commit()

        admin_role = session.query(Roles).filter(Roles.name == "admin").first()
        if not admin_role:
            admin_role = Roles(name="admin")
            session.add(admin_role)
            session.commit()

        new_assignment = UsersRoles(user_id=admin_user.id, role_id=admin_role.id)
        session.add(new_assignment)
        session.commit()
