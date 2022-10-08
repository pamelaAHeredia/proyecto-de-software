from src.models.database import db
from src.models.auth.role import Role
from src.models.auth.permission import Permission


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