from src.models.database import db
from src.models.auth.user import User
from src.models.auth.role import Role
from src.models.auth.permission import Permission


def list_users():
    """Función que retorna la lista de todos los Usuarios de la Base de Datos"""
    return User.query.all()


def create_user(**kwargs):
    """Función que instancia un Usuario, lo agrega a la Base de Datos y lo retorna"""
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def create_role(**kwargs):
    """Función que instancia un Rol, lo agrega a la Base de Datos y lo retorna"""
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role


def create_permission(*args):
    """Función que instancia un Permiso, lo agrega a la Base de Datos y lo retorna"""
    permission = Permission(name=args)
    db.session.add(permission)
    db.session.commit()
    return permission