from src.models.auth.user import User

def list_users():
    return User.query.all()

