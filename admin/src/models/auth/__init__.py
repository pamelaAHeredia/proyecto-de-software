from src.models.database import db
from src.models.auth.user import User
from src.models.auth.role import Role
from src.models.auth.permission import Permission


def list_users():
    return User.query.all()


def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role


def create_permission(*args):
    permission = Permission(name=args)
    db.session.add(permission)
    db.session.commit()
    return permission
