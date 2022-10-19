from src.models.auth.user import User
from src.models.auth.role import Role
from src.services.utils import verify_pass


def find_user_by_mail_and_pass(email, password):
    """Función que retorna si existe un usuario que coincida el email y contraseña"""
    user = User.query.filter_by(email=email).first()
    if user and verify_pass(user.password, password):
        return user
    else:
        return None

