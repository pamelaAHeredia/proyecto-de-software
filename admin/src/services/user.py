from src.models.database import db
from src.models.auth.user import User


class UserService:
    """Clase que representa el manejo de los usuarios"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    def list_users(self):
        """Función que retorna la lista de todos los Usuarios de la Base de Datos"""
        return User.query.all()

    def create_user(
        self, email, username, password, is_active, first_name, last_name, blocked
    ):
        """Función que instancia un usuario, si no existe en la BD, y lo retorna"""
        user = User(
            email, username, password, is_active, first_name, last_name, blocked
        )
        if not self.find_user_byEmail(email):
            if not self.find_user_byUsername(username):
                db.session.add(user)
                db.session.commit()
                return user
            return None
        return None

    def find_user_byEmail(self, email):
        return User.query.filter_by(email=email).first()

    def find_user_byUsername(self, username):
        return User.query.filter_by(username=username).first()

    def find_user_by_id(self, id):
        return User.query.get(id)

    def update_user(self, id, email, username, first_name, last_name):
        """Función que actualiza los datos de un usuario, si el mail y el nombre de usuarios ingresados son válidos"""
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
            return None
        return None

    def block_user(self, id):
        user = self.find_user_by_id(id)
        """Si el usuario está bloqueado lo desbloquea, y viceversa"""
        if user.blocked:
            user.blocked = False
        else:
            user.blocked = True
        db.session.commit()
        return user
