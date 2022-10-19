from src.models.database import db
from src.models.auth.user import User
from src.models.auth.role import Role

from src.models.auth.permission import Permission
from src.services.paginator import Paginator
from src.services.utils import verify_pass
from src.errors import database


class UserService:
    """Clase que representa el manejo de los usuarios"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    def list_users(self):
        """
        Retorna la lista de todos los Usuarios de la Base de Datos
        """
        return User.query.order_by(User.id)

    def list_paginated_users(self, page: int, items_per_page: int, endpoint: str, filter_by: str) -> Paginator:
        """
        Retorna el paginador de los usuarios del sistema
        """
        if filter_by == "activo":
            users = self.find_active_users()
        elif filter_by == "bloqueado":
             users = self.find_blocked_users()
        else:
            users = self.list_users()
        return Paginator(users, page, items_per_page, endpoint)

    def create_user(self, email, username, password, first_name, last_name, roles):
        """
        Función que instancia un usuario, si no existe en la BD, y lo retorna
        """
        if not self.find_user_byEmail(email):
            if not self.find_user_byUsername(username):
                user = User(email, username, password, first_name, last_name, [])
                for role in roles:
                    user.roles.append(role)
                db.session.add(user)
                db.session.commit()
            else:
                raise database.ExistingData(
                    info="Error", message="El usuario que intenta agregar ya existe."
                )
        else:
            raise database.ExistingData(
                info="Error", message="El email que intenta agregar ya existe."
            )
        return user

    def find_user_byEmail(self, email):
        return User.query.filter_by(email=email).first()

    def find_by_username_and_pass(self, username, password):
        """
        Función que retorna si existe un usuario que coincida el email y contraseña
        """
        user = self.find_user_byUsername(username)
        if user:
            if verify_pass(user.password, password):
                if user.is_active == True:
                    return user
                else:
                    raise database.PermissionDenied(
                        info="No se pudo iniciar sesión.",
                        message="El usuario se encuentra bloqueado. Contáctese con un administador para solucionarlo",
                    )
            else:
                raise database.PermissionDenied(
                    info="No se pudo iniciar sesión.", message="Contraseña incorrecta."
                )
        else:
            raise database.PermissionDenied(
                info="No se pudo iniciar sesión.", message="Usuario incorrecto."
            )

    def find_user_byUsername(self, username):
        return User.query.filter_by(username=username).first()

    def find_user_by_id(self, id):
        return User.query.get(id)

    def update_user(self, id, email, username, first_name, last_name):
        """Actualiza los datos de un usuario, si el mail y el nombre de usuarios ingresados son válidos"""
        mail_found = self.find_user_byEmail(email)
        username_found = self.find_user_byUsername(username)
        if not mail_found or int(id) == mail_found.id:
            if not username_found or int(id) == username_found.id:
                user = self.find_user_by_id(id)
                user.email = email
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                db.session.commit()
                return user
            else:
                raise database.ExistingData(
                    info="Error", message="El usuario que intenta agregar ya existe."
                )
        raise database.ExistingData(
            info="Error", message="El Email que intenta agregar ya existe."
        )

    def block_user(self, id, user_session):
        blocker_id = self.find_user_by_id(user_session)
        user = self.find_user_by_id(id)
        role = self.find_role_by_name("Administrador")

        """Si el usuario no es un administrador y está bloqueado lo desbloquea, y viceversa"""

        if not user.roles.__contains__(role):
            if not blocker_id == user.id:
                print(blocker_id, user.id)
                if user.is_active:
                    user.is_active = False
                else:
                    user.is_active = True
                db.session.commit()
            else:
                raise database.PermissionDenied(
                    info="Permiso Denegado",
                    message="No se puede bloquear a sí mismo.",
                )
        else:
            raise database.PermissionDenied(
                info="Permiso Denegado",
                message="No se puede bloquear un usuario con rol de Administrador.",
            )
        return user

    def find_active_users(self):
        """Retorna todos los usuarios, que no están bloqueados."""
        return User.query.filter_by(is_active=True)

    def find_blocked_users(self):
        """Retorna todos los usuarios, que están bloqueados."""
        return User.query.filter_by(is_active=False)

    # No va?
    def deactivate_user(self, id):
        user = self.find_user_by_id(id)
        """Si el usuario está activo lo desbloquea, y viceversa"""
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        db.session.commit()
        return user

    def delete(self, id, session_id):
        user = self.find_user_by_id(id)
        if user.id != session_id:
            db.session.delete(user)
            db.session.commit()
        else:
            raise database.PermissionDenied(
                info="Permiso Denegado", message="No puede eliminar su propio usuario."
            )

    def create_role(self, name):
        """Función que instancia un Rol, lo agrega a la Base de Datos y lo retorna"""
        role = Role(name)
        db.session.add(role)
        db.session.commit()
        return role

    def create_permission(self, name):
        """Función que instancia un Permiso, lo agrega a la Base de Datos y lo retorna"""
        permission = Permission(name)
        db.session.add(permission)
        db.session.commit()
        return permission

    def add_role(self, id, role_name):
        """Permite asignar roles a un usuario."""
        user = self.find_user_by_id(id)
        roles = user.roles
        role = self.find_role_by_name(role_name)
        if not roles.__contains__(role):
            user.roles.append(role)
        else:
            raise database.ExistingData(
                info="Los datos ya existen", message="El usuario ya tiene este rol."
            )
        db.session.commit()

    def find_role_by_name(self, name):
        """Busca un rol por su nombre y lo retorna, si lo encuentra."""
        return Role.query.filter_by(name=name).first()

    def remove_role(self, id, roles):
        """Elimina un rol de la lista de roles de un usuario, si tiene más de un rol."""
        user = self.find_user_by_id(id)

        if len(user.roles) > 1:
            role = self.find_role_by_name(roles)
            user.roles.remove(role)
            db.session.commit()
        else:
            raise database.PermissionDenied(
                info="Permiso Denegado", message="El usuario debe tener,mínimo, un rol."
            )
        return user

    def list_user_roles(self, id):
        """Retorna todos los roles de un usuario."""
        user = self.find_user_by_id(id)
        return user.roles
