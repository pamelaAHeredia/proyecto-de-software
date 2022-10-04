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


# perteneciente a usuarios

#Buscar usuario por mail 
def find_user_byEmail(mail):
    user = db.session.query(User) \
        .filter(User.email == mail) \
        .first()
    return user

#función que valida que el mail ingresado no existe en la bd
def mail_not_exists(mail):
    user = find_user_byEmail(mail)
    return user == None

#Buscar usuario por username 
def find_user_byUsername(userName):
    user = db.session.query(User) \
        .filter(User.username == userName) \
        .first()
    return user 

#función que valida que el nombre de usuario ingresado no existe en la bd
def username_not_exists(userName):
    user = find_user_byUsername(userName)
    return user == None

def delete_user(id):
    user = find_user(id)
    db.session.delete(user)
    db.session.commit()

def find_user(id):
    user = db.session.query(User) \
        .filter(User.id == id) \
        .first()
    return user

def update_user(id, **kwargs):
    user = find_user(id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
