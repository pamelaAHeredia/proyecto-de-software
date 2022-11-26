from functools import wraps
import jwt
from flask import current_app, jsonify, request
from src.services.user import UserService


_user_service = UserService()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return jsonify({"message": "Token requerido"}), 401
        try:
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            current_user = _user_service.find_user_byUsername(data["user"])
        except:
            return jsonify({"message": "Token invalido"}), 401
        return f(current_user, *args, **kwargs)
    return decorated