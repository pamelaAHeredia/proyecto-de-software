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
            logged_user = User.query.filter_by(id=session.get("user")).first()
            for r in logged_user.roles:
                for p in r.permissions:
                    if p.name == perms:
                        return f(*args, **kwargs)
            return abort(403)
        return wrapper
    return decorate


def is_administrator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(id=session.get("user")).first()
        for r in user.roles:
            if r.name == "Administrador":
                return f(*args, **kwargs)
        return abort(403)
    return decorated_function

def is_operator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(id=session.get("user")).first()
        for r in user.roles:
            if r.name == "Operador":
                return f(*args, **kwargs)
        return abort(403)
    return decorated_function

def is_member(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(id=session.get("user")).first()
        for r in user.roles:
            if r.name == "Socio":
                return f(*args, **kwargs)
        return abort(403)
    return decorated_function

def is_administrator_template(session):
    user = User.query.filter_by(id=session.get("user")).first()
    for r in user.roles:
        if r.name == "Administrador":
            return True
    return False

def is_operator_template(session):
    user = User.query.filter_by(id=session.get("user")).first()
    for r in user.roles:
        if r.name == "Operador":
            return True
    return False

def is_member_template(session):
    user = User.query.filter_by(id=session.get("user")).first()
    for r in user.roles:
        if r.name == "Socio":
            return True
    return False

def is_admin(id):
    service = UserService()
    user = service.find_user_by_id(id)
    admin = service.find_role_by_name("Administrador")
    return user.roles.__contains__(admin)
    
def can_do_it(session, perm):
    user = User.query.filter_by(id=session.get("user")).first()
    for r in user.roles:
        for p in r.permissions:
                if p.name == perm:
                    return True
    return False
