from functools import wraps
from flask import session, abort
from src.models.auth.user import User
from src.services.user import UserService


def is_authenticated(session):
    return session.get("user") != None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function


def verify_permission(perms):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            logged_user = User.query.filter_by(email=session.get("user")).first()
            for r in logged_user.roles:
                for p in r.permissions:
                    if p.name == perms:
                        return f(*args, **kwargs)
            return abort(403)
        return wrapper
    return decorate

